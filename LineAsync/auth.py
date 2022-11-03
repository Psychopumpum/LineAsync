from .server import Server
from .transport import THttpClient

from frugal.context import FContext
from frugal.provider import FServiceProvider
from frugal.protocol import FProtocol, FProtocolFactory

from thrift.transport.TTransport import TMemoryBuffer, TTransportException
from thrift.protocol.TCompactProtocol import TCompactProtocolAcceleratedFactory

from LineFrugal.SecondaryService.ttypes import *
from LineFrugal.SecondaryService import (
    FSecondaryQrCodeLoginServiceClient,
    FSecondaryQrCodeLoginPermitServiceClient,
    FSecondaryQrCodeLoginPermitNoticeServiceClient
)

from LineFrugal.TalkService import FTalkServiceClient

import sys, os

class Connection(object):

    def __init__(self, url, service, timeout = None, **kwargs):
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
            return await rfr(self.ctx, *arg, **kws)
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
            "x-lap": "5", "Content-Type": "application/x-thrift; protocol=TCOMPACT",
            "x-lam": "w", "x-las": "F"
        })

    async def loginWithQrCode(self):
        login = Connection(
            self.server.TALK_SERVER_HOST + self.server.SECONDARY_QR_LOGIN,
            FSecondaryQrCodeLoginServiceClient,
            60000,
            request = "httpx"
        )
        login.transport.setCustomHeaders(self.server.talkHeaders)
        auth = await login.call("createSession", CreateQrSessionRequest())
        qrCode = await login.call("createQrCode", CreateQrCodeRequest(auth.authSessionId))
        verify = Connection(
            self.server.TALK_SERVER_HOST + self.server.SECONDARY_VERIFY_LOGIN,
            FSecondaryQrCodeLoginPermitNoticeServiceClient,
            60000,
            request = "httpx"
        )
        self.server.talkHeaders.update({
            "X-Line-Access": auth.authSessionId
        })
        verify.transport.setCustomHeaders(self.server.talkHeaders)
        callback = f"{qrCode.callbackUrl}{self.server.generateSecret()}"
        print(f"CallbackURL: {callback}\nLongPollingMax: {qrCode.longPollingMaxCount}\nInterval: {qrCode.longPollingIntervalSec}")
        os.system(f"go run qrcode.go {callback}")
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
        except Exception as e:
            print(e)
            result = await login.call("qrCodeLogin", QrCodeLoginRequest(auth.authSessionId, "Psychopumpum", True))
            self.accessToken = result.accessToken
        self.server.talkHeaders.update({
            "X-Line-Access": self.accessToken
        })
        self.certificate = result.certificate
        return self.loginWithAccessToken()

    def loginWithAccessToken(self):
        self.server.talkHeaders.update({
            "X-Line-Access": self.accessToken
        })
        self.talk = Connection(self.server.TALK_SERVER_HOST + "/S4", FTalkServiceClient, 120000, request = "httpx")
        self.talk.transport.setCustomHeaders(self.server.talkHeaders)
        self.server.pollHeaders.update({
            "X-Line-Access": self.accessToken
        })
        self.poll = Connection(self.server.TALK_SERVER_HOST + "/P4", FTalkServiceClient, 4000, request = "httpx")
        self.poll.transport.setCustomHeaders(self.server.pollHeaders)