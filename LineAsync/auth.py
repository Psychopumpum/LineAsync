from .server import Server
from .transport import THttpClient

from frugal.context import FContext
from frugal.provider import FServiceProvider
from frugal.protocol import FProtocol, FProtocolFactory

from thrift.transport.TTransport import TMemoryBuffer, TTransportException
from thrift.protocol.TCompactProtocol import TCompactProtocolAcceleratedFactory

from LineFrugal import (
    FTalkServiceClient,
    FAuthServiceClient,
    FSecondaryQrCodeLoginServiceClient,
    FSecondaryQrCodeLoginPermitServiceClient,
    FSecondaryQrCodeLoginPermitNoticeServiceClient
)
from LineFrugal.ttypes import *

import sys, os, rsa, livejson, asyncio

class Connection(object):

    def __init__(self, url, service, timeout = None, **kwargs):
        self.loop             = asyncio.get_event_loop()
        self.ctx              = FContext()
        self.transport        = THttpClient(url, timeout = timeout, **kwargs)
        self.protocol_factory = TCompactProtocolAcceleratedFactory()
        self.wrapper_factory  = FProtocolFactory(self.protocol_factory)
        self.service_provider = FServiceProvider(self.transport, self.wrapper_factory)
        self._client          = service(self.service_provider)

    async def call(self, rfunc: str, *arg, **kws) -> callable:
        assert isinstance(rfunc, str), f"Function name must be str and not {type(rfunc).__name__}"
        rfr = getattr(self._client, rfunc, None)
        if rfr:
            return await asyncio.create_task(rfr(self.ctx, *arg, **kws))
        raise Exception("Function name is not defined.")

class Auth(Server):

    def __init__(self):
        self.server = Server(self.appType, self.secondary)
        if self.appName:
            self.server.APP_NAME = self.appName
            self.server.USER_AGENT = f"Line/" + self.server.APP_NAME.split('\t')[1]
        self.server.setHeadersWithDict({
            "User-Agent": self.server.USER_AGENT,
            "X-Line-Application": self.server.APP_NAME,
            "x-lal": "en_GB",
            "x-lpv": "1",
            "x-lac": "51010"
        })
        self.server.setPollHeadersWithDict({
            "x-lal": "en_GB",
            "x-lpv": "1", "x-lac": "51010",
            "User-Agent": self.server.USER_AGENT,
            "X-Line-Application": self.server.APP_NAME,
            "x-lap": "5", "Content-Type": "application/x-thrift",
            "x-lam": "w", "x-las": "F"
        })

    async def loginWithQrCode(self):
        login = Connection(
            self.server.TALK_SERVER_HOST + self.server.SECONDARY_QR_LOGIN,
            FSecondaryQrCodeLoginServiceClient,
            60000,
            request = "httpx"
        )
        hr = self.server.talkHeaders
        if self.send_to:
            if hr.get('X-Line-Access'):del hr['X-Line-Access']
        login.transport.setCustomHeaders(hr)
        if self.appType == "CHROMEOS":
            login.transport.setCustomHeaders({ "origin": "chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc"})
        auth = await login.call("createSession", CreateQrSessionRequest())
        qrCode = await login.call("createQrCode", CreateQrCodeRequest(auth.authSessionId))
        verify = Connection(
            self.server.TALK_SERVER_HOST + self.server.SECONDARY_VERIFY_LOGIN,
            FSecondaryQrCodeLoginPermitNoticeServiceClient,
            60000,
            request = "httpx"
        )
        hr.update({
            "X-Line-Access": auth.authSessionId
        })
        verify.transport.setCustomHeaders(hr)
        if self.appType == "CHROMEOS":
            verify.transport.setCustomHeaders({
                "origin": "chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc"
            })
        self.secret, secret = self.server.generateSecret()
        callback = f"{qrCode.callbackUrl}{secret}"
        if not self.send_to:
            print(f"CallbackURL: {callback}\nLongPollingMax: {qrCode.longPollingMaxCount}\nInterval: {qrCode.longPollingIntervalSec}")
            os.system(f"go run qrcode.go {callback}")
        else:
            p = await self.sendMessage(self.send_to, callback)
        try:
            verifyQrCode = await verify.call(
                "checkQrCodeVerified",
                CheckQrCodeVerifiedRequest(
                    auth.authSessionId
                )
            )
        except TTransportException as e:
            if e.message == "request timeout":
                sys.exit("Request has been timeout.")
        try:
            await login.call("verifyCertificate", VerifyCertificateRequest(auth.authSessionId, self.certificate))
        except Exception as e:
            pin = await login.call("createPinCode", CreatePinCodeRequest(auth.authSessionId))
            print(f"Pincode: {pin.pinCode}")
            try:
                await verify.call("checkPinCodeVerified", CheckPinCodeVerifiedRequest(auth.authSessionId))
            except TTransportException as e:
                if e.message == "request timeout":
                    sys.exit("Request has been timeout.")
        try:
            result = await login.call("qrCodeLoginV2", QrCodeLoginV2Request(auth.authSessionId, "Psychopumpum", "BOTS", True))
            self.accessToken = result.tokenV3IssueResult.accessToken
            self.refreshToken = result.tokenV3IssueResult.refreshToken
        except Exception as e:
            print(e)
            result = await login.call("qrCodeLogin", QrCodeLoginRequest(auth.authSessionId, "Psychopumpum", True))
            self.accessToken = result.accessToken
            self.refreshToken = None
        self.server.talkHeaders.update({
            "X-Line-Access": self.accessToken
        })
        self.certificate = result.certificate
        self.metaData = result.metaData
        return await self.loginWithAccessToken()

    async def loginWithCredential(self, email, passwd):
        if self.appType:
            if not self.systemName:
                self.systemName = self.server.SYSTEM_NAME[self.appType]
            else:
                self.systemName = self.systemName
        else:
            self.systemName = "Psychopumpum"
        if self.server.EMAIL_REGEX.match(email):
            self.provider = IdentityProvider.LINE
        else:
            self.provider = IdentityProvider.NAVER_KR
        tauth = Connection(
            "https://ga2.line.naver.jp/api/v4/TalkService.do",
            FAuthServiceClient,
            60000,
            request = "httpx"
        )
        tauth.transport.setCustomHeaders(self.server.talkHeaders)
        rsaKey  = await tauth.call('getRSAKeyInfo', self.provider)
        message = f"{chr(len(rsaKey.sessionKey))}{rsaKey.sessionKey}{chr(len(email))}{email}{chr(len(passwd))}{passwd}".encode("utf-8")
        pub_key = rsa.PublicKey(int(rsaKey.nvalue, 16), int(rsaKey.evalue, 16))
        crypto  = rsa.encrypt(message, pub_key).hex()
        auth = Connection(
            "https://ga2.line.naver.jp/api/v4p/rs",
            FAuthServiceClient,
            60000,
            request = "httpx"
        )
        auth.transport.setCustomHeaders(self.server.talkHeaders)
        lReq = self.__loginRequest(0, {
            'identityProvider': self.provider,
            'identifier': rsaKey.keynm,
            'password': crypto,
            'keepLoggedIn': self.keepLoggedIn,
            'systemName': self.systemName,
            'certificate': self.certificate,
            'e2eeVersion': 0
        })
        '''try:
            result = await auth.call('loginV2', lReq)
        except TalkException as e:'''
        result = await auth.call('loginZ', lReq)
        if result.type == LoginResultType.REQUIRE_DEVICE_CONFIRM:
            print(f"Pincode: {result.pinCode}")
            self.server.setHeaders('X-Line-Access', result.verifier)
            getAccessKey = await self.server.request('GET', self.server.TALK_SERVER_HOST_SECONDARY + "/Q", headers = self.server.talkHeaders)
            getAccessKey = getAccessKey["json"]
            lReq = self.__loginRequest(1, {
                'keepLoggedIn': self.keepLoggedIn,
                'verifier': getAccessKey['result']['verifier'],
                'e2eeVersion': 0,
                'systemName': self.systemName,
                'modelName': 'iPadOS'
            })
            '''try:
                result = await auth.call('loginV2', lReq)
            except TalkException as e:'''
            result = await auth.call('loginZ', lReq)
        print(result)
        self.accessToken, self.certificate = result.authToken, result.certificate
        return self.loginWithAccessToken(self.accessToken)

    def __loginRequest(self, type, data):
        lReq = LoginRequest()
        if type == 0:
            lReq.type             = 0
            lReq.identityProvider = data['identityProvider']
            lReq.identifier       = data['identifier']
            lReq.password         = data['password']
            lReq.keepLoggedIn     = data['keepLoggedIn']
            lReq.systemName       = data['systemName']
            lReq.certificate      = data['certificate']
            lReq.e2eeVersion      = data['e2eeVersion']
        elif type == 1:
            lReq.type             = 1
            lReq.keepLoggedIn     = data.get('keepLoggedIn')
            lReq.identityProvider = data.get('identityProvider')
            lReq.accessLocation   = data.get('accessLocation')
            lReq.systemName       = data.get('systemName')
            lReq.verifier         = data.get('verifier')
            lReq.e2eeVersion      = data.get('e2eeVersion')
        elif type == 2:
            lReq.type             = 2
            lReq.identityProvider = data['identityProvider']
            lReq.identifier       = data['identifier']
            lReq.password         = data['password']
            lReq.keepLoggedIn     = data['keepLoggedIn']
            lReq.systemName       = data['systemName']
            lReq.certificate      = data['certificate']
            lReq.secret           = data['secret']
            lReq.e2eeVersion      = data['e2eeVersion']
        return lReq

    async def loginWithAccessToken(self):
        self.server.talkHeaders.update({
            "X-Line-Access": self.accessToken
        })
        if self.appType == "CHROMEOS":
            self.server.talkHeaders.update({
                "origin": "chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc"
            })
        self.talk = Connection(self.server.TALK_SERVER_HOST + "/S4", FTalkServiceClient, 120000, request = "httpx")
        self.talk.transport.setCustomHeaders(self.server.talkHeaders)
        self.server.pollHeaders.update({
            "X-Line-Access": self.accessToken,
            "Connection": "keep-alive"
        })
        if self.appType == "CHROMEOS":
            self.server.pollHeaders.update({
                "origin": "chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc"
            })
        self.poll = Connection(self.server.TALK_SERVER_HOST + "/P4", FTalkServiceClient, 4000, request = "httpx")
        self.poll.transport.setCustomHeaders(self.server.pollHeaders)
        self.auth = Connection(self.server.TALK_SERVER_HOST + '/RS4', FAuthServiceClient, 4000, request = "httpx")
        self.auth.transport.setCustomHeaders(self.server.talkHeaders)
        self.profile = await self.talk.call('getProfile', 4)
        self.settings = livejson.File(f"{self.profile.mid}.json", True, True, 4)
        if not self.settings.get("login"):
            self.settings["login"] = {}
        print(self.appType)
        if not self.settings["login"].get(self.appType):
            self.settings["login"][self.appType] = {}
            self.settings["login"][self.appType].update({
                "accessToken": self.accessToken,
                "refreshToken": self.refreshToken if self.refreshToken else '',
                "mid": self.profile.mid,
                "certificate": self.certificate if self.certificate else '',
                "secret": self.secret if self.secret else '',
                **self.metaData
            })
        else:
            self.settings["login"][self.appType].update({
                "accessToken": self.accessToken,
            })
        self.e2ee = await self.talk.call('negotiateE2EEPublicKey', self.profile.mid)
        if self.e2ee.publicKey:
            key = self.e2ee.publicKey
            return await self.talk.call('removeE2EEPublicKey', E2EEPublicKey(
                key.version,
                key.keyId,
                key.keyData,
                key.createdTime
            ))
