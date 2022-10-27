# -*- coding: utf-8 -*-
from thrift.transport.TTransport import TMemoryBuffer
from thrift.protocol.TCompactProtocol import TCompactProtocolAcceleratedFactory
from LAsyncClient.transport import THttpClient
from LineFrugal.CoinService import FCoinServiceClient
from LineFrugal.CoinService.ttypes import *
from frugal.provider import FServiceProvider
from frugal.context import FContext
from frugal.protocol import FProtocol

class LegyProtocol(FProtocol):
    # We dont need frugal default body header
    def write_request_headers(self,*args,**kws):
        pass
    def write_response_headers(self,*args,**kws):
        pass
    def _write_headers(self, *args, **kws):
        pass
    def read_request_headers(self):
        pass
    def read_response_headers(self, *args, **kws):
        pass

import asyncio

class LegyProtocolFactory(object):
    def __init__(self, t_protocol_factory):
        """
        Args:
            t_protocol_factory: Thrift TProtocolFactory.
        """
        self._t_protocol_factory = t_protocol_factory

    def get_protocol(self, transport):
        return LegyProtocol(self._t_protocol_factory.getProtocol(transport))

class Connection(object):

    def __init__(self):
        self.context = FContext()
        self.transport = THttpClient("https://ga2.line.naver.jp" + "/COIN4", request = "httpx")
        self.protocol_factory = TCompactProtocolAcceleratedFactory()
        self.wrapper_factory  = LegyProtocolFactory(self.protocol_factory)
        self.service_provider = FServiceProvider(self.transport, self.wrapper_factory)
        self.client = self.LiffClients()

    def call(self, rfunc: str, *args, **kws) -> callable:
        assert isinstance(rfunc, str), 'Function name must be str not '+type(rfunc).__name__
        rfr = getattr(self.client, rfunc, None)
        if rfr:
            return rfr(self.context, *args, **kws)
        else:
            raise Exception(rfunc + ' is not exist')
	
    def LiffClients(self):
        return FCoinServiceClient(self.service_provider)
	

c = Connection()
c.transport.setCustomHeaders({
    "X-Line-Access": "ua4d14b263eaaf5c3f8a28c23fbc648f5:aWF0OiAxNjM4ODM1NzA0MzEzCg==..KFKhajdqfVXUipKV3OHX6UQVWQk=",
    "X-Line-Application": "IOS\t12.17.1\tiOS\t15.0",
    "x-lal": "en_GB",
    "User-Agent": "Line/12.17.1",
})

async def getTotalCoinBalance():
    return await c.call("getTotalCoinBalance",
        GetTotalCoinBalanceRequest(
            2
        )
    )

a = asyncio.get_event_loop()
print(a.run_until_complete(getTotalCoinBalance()))
print(c.transport.headers)