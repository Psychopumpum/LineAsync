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
        self._session        = httpx.AsyncClient(http2 = True)

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

    async def request(self, method: str, url, *args, **kwargs):
        method = method.upper()
        result = {}
        async with self._session as client:
            if method == "GET":
                response = await client.get(url, *args, timeout = None, **kwargs)
            elif method == "POST":
                response = await client.post(url, *args, **kwargs)
            elif method == "PUT":
                response = await client.put(url, *args, **kwargs)
            elif method == "HEAD":
                response = await client.head(url, *args, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, *args, timeout = None, **kwargs)
            result.update({
                'code': response.status_code,
                'text': response.text,
                'json': response.json()
            })
            return result

    def generateSecret(self, email = False):
        privateKey = curve.generatePrivateKey(os.urandom(32))
        secret     = urllib.parse.quote(base64.b64encode(curve.generatePublicKey(privateKey)).decode())
        if email:
            return f"{secret.encode()}"
        return f"?secret={secret}&e2eeVersion=1"