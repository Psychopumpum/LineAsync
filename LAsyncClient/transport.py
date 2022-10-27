# -*- coding: utf-8 -*-
import async_timeout, asyncio, aiohttp, httpx, inspect
from aiohttp.client import ClientSession

from thrift.transport.TTransport import TTransportBase
from thrift.transport.TTransport import TMemoryBuffer
from thrift.transport.TTransport import TTransportException

from frugal.aio.transport import FTransportBase
from frugal.context import FContext
from frugal.aio.transport.http_transport import FHttpTransport
from frugal.exceptions import TTransportExceptionType

from six.moves import urllib
from httplib2 import Response, Http, ProxyInfo

class THttpClient(FHttpTransport):

    code    = None
    message = None
    headers = None

    def __init__(self, url, timeout = 5000, loop = None, request = "httpx", proxy_host = None, proxy_port = None):
        super().__init__(0)
        self.custom_request = request
        self.setTimeout(timeout)
        self.proxy_host, self.proxy_port = proxy_host, proxy_port
        if self.custom_request  == "aiohttp":
            self._url = url
            pass
        else:
            parsed        = urllib.parse.urlparse(url)
            self.scheme = parsed.scheme
            assert self.scheme in ('http', 'https')
            if self.scheme == 'http':
                self.port = parsed.port or 80
            elif self.scheme == 'https':
                self.port = parsed.port or 443
            self.host = parsed.hostname
            self.path = parsed.path
            if parsed.query:
                self.path += '?%s' % parsed.query
            self.__url = '%s://%s:%s%s' % (self.scheme, self.host, self.port, self.path)
            if self.custom_request  == "httplib2":
                self.client   = Http(proxy_info=ProxyInfo(proxy_type = 3, proxy_host = self.proxy_host, proxy_port = self.proxy_port), timeout = self._timeout)
                self.response = Response
            elif self.custom_request == "httpx":
                self.client   = httpx.AsyncClient(base_url='%s://%s' % (self.scheme, self.host), http2 = True, timeout = self._timeout)
        self._url = url
        self._loop = loop if loop else asyncio.get_event_loop()
        self._headers = {
            'Content-Type': 'application/x-thrift',
            'Accept': 'application/x-thrift',
        }

    def setTimeout(self, timeout):
        self._timeout = timeout

    def setCustomHeaders(self, headers: dict) -> dict:
        self._headers.update(**headers)

    async def request(self, context: FContext, payload) -> TTransportBase:
        payload = payload[4:] 
        self._payload = payload
        self._preflight_request_check(payload)
        data = await self._make_request(context, self._payload)
        if self.code == 400: 
            raise TTransportException(
                type=400, 
                message='Bad request: '+str(text) + ' :: '+ str(payload))
        elif self.code == 403:
            raise TTransportException(
                type=403, 
                message='Forbidden: '+str(text))
        elif self.code == 404:
            raise TTransportException(
                type=404,
                message='Not Found: '+str(text))
        elif self.code == 410:
            pass
        elif self.code == 500:
            raise TTransportException(
                type=500,
                message='Backend Error: '+str(text))
        elif self.code >= 300:
            raise TTransportException(
                type=TTransportExceptionType.UNKNOWN,
                message='request errored with {0} and message {1}'.format(
                    status, str(text)
                )
            )
        return TMemoryBuffer(self.response)

    async def _make_request(self, context:FContext, payload):
        sem = asyncio.Semaphore(200)
        conn = aiohttp.TCPConnector(use_dns_cache = True, loop = self._loop, limit = 0)
        self._headers.update({"Content-Length": str(len(payload))})
        async with sem:
            try:
                with async_timeout.timeout(self._timeout / 1000):
                    if self.custom_request == "httpx":
                        response = await self.client.request("POST", self.path, data = payload, headers = self._headers)
                        if inspect.iscoroutine(response):
                            self.response = await response.read()
                        else:
                            self.response = response.read()
                        self.__set_response(response)
                        return self.response
                    elif self.custom_request == "httplib2":
                        headers, self.response = self.client.request(self._url, "POST", body = payload, headers = self._headers)
                        self.__set_response(headers)
            except asyncio.TimeoutError:
                raise TTransportException(
                    type=TTransportExceptionType.TIMED_OUT,
                    message='request timed out'
                )

    def __set_response(self, response):
        if self.custom_request == "gevent":
            self.code = response.status_code
            self.message = response.status_message
            self.headers = response.headers
        elif self.custom_request == "httplib2":
            self.code = response.status
            self.message = response.reason
            self.headers = response
        else:
            self.code = response.status_code
            self.message = response.reason_phrase
            self.headers = response.headers