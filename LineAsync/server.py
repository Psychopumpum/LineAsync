from .config import Config
import re, os
import httpx, time, base64
import axolotl_curve25519 as curve

from six.moves import urllib

class Server(Config):

    EMAIL_REGEX  = re.compile(r"[^@]+@[^@]+\.[^@]+")

    def __init__(self, appType = None, secondary = False):
        Config.__init__(self, appType, secondary)
        self.talkHeaders     = {}
        self.timelineHeaders = {}
        self.liffHeaders     = {}
        self.pollHeaders     = {}
        limits = httpx.Limits(max_keepalive_connections=10, max_connections=10)
        self._session        = httpx.AsyncClient(limits = limits, http2 = True)

    def setHeadersWithDict(self, headersDict):
        self.talkHeaders.update(headersDict)

    def setHeaders(self, argument, value):
        self.talkHeaders[argument] = value

    def setPollHeadersWithDict(self, headersDict):
        self.pollHeaders.update(headersDict)

    def setPollHeaders(self, key, val):
        self.pollHeaders[key] = val

    def setTimelineHeadersWithDict(self, headersDict):
        self.timelineHeaders.update(headersDict)

    def setTimelineHeaders(self, argument, value):
        self.timelineHeaders[argument] = value

    def setLiffHeadersWithDict(self, headersDict):
        self.liffHeaders.update(headersDict)

    def setLiffHeaders(self, key, value):
        self.liffHeaders[key] = value

    def additionalHeaders(self, source, newSource):
        headerList = {}
        headerList.update(source)
        headerList.update(newSource)
        return headerList

    async def request(self, method: str, url, arr: str = "json", *args, **kwargs):
        method = method.upper()
        result = {}
        if method == "GET":
            response = await self._session.get(url, *args, timeout = None, **kwargs)
        elif method == "POST":
            response = await self._session.post(url, *args, timeout = None, **kwargs)
        elif method == "PUT":
            response = await self._session.put(url, *args, **kwargs)
        elif method == "HEAD":
            response = await self._session.head(url, *args, **kwargs)
        elif method == "DELETE":
            response = await self._session.delete(url, *args, timeout = None, **kwargs)
        if arr == 'json':
            result.update({
                'code': response.status_code,
                'text': response.text,
                'json': response.json(),
                'headers': response.headers
            })
            return result
        return response

    def generateSecret(self, email = False):
        privateKey = curve.generatePrivateKey(os.urandom(32))
        secret     = urllib.parse.quote(base64.b64encode(curve.generatePublicKey(privateKey)).decode())
        if email:
            return f"{secret.encode()}"
        return (privateKey, f"?secret={secret}&e2eeVersion=1")