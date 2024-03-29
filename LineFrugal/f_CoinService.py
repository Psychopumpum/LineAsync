#
# Autogenerated by Frugal Compiler (3.16.5)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#



import asyncio
from datetime import timedelta
import inspect

from frugal.aio.processor import FBaseProcessor
from frugal.aio.processor import FProcessorFunction
from frugal.exceptions import TApplicationExceptionType
from frugal.exceptions import TTransportExceptionType
from frugal.middleware import Method
from frugal.transport import TMemoryOutputBuffer
from frugal.util.deprecate import deprecated
from thrift.Thrift import TApplicationException
from thrift.Thrift import TMessageType
from thrift.transport.TTransport import TTransportException
from .ttypes import *


class Iface(object):

    async def getTotalCoinBalance(self, ctx, request):
        """
        Args:
            ctx: FContext
            request: GetTotalCoinBalanceRequest
        """
        pass

    async def getCoinProducts(self, ctx, request):
        """
        Args:
            ctx: FContext
            request: GetCoinProductsRequest
        """
        pass

    async def reserveCoinPurchase(self, ctx, request):
        """
        Args:
            ctx: FContext
            request: CoinPurchaseReservation
        """
        pass

    async def getCoinPurchaseHistory(self, ctx, request):
        """
        Args:
            ctx: FContext
            request: GetCoinHistoryRequest
        """
        pass

    async def getCoinUseAndRefundHistory(self, ctx, request):
        """
        Args:
            ctx: FContext
            request: GetCoinHistoryRequest
        """
        pass


class Client(Iface):

    def __init__(self, provider, middleware=None):
        """
        Create a new Client with an FServiceProvider containing a transport
        and protocol factory.

        Args:
            provider: FServiceProvider
            middleware: ServiceMiddleware or list of ServiceMiddleware
        """
        middleware = middleware or []
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]
        self._transport = provider.get_transport()
        self._protocol_factory = provider.get_protocol_factory()
        middleware += provider.get_middleware()
        self._methods = {
            'getTotalCoinBalance': Method(self._getTotalCoinBalance, middleware),
            'getCoinProducts': Method(self._getCoinProducts, middleware),
            'reserveCoinPurchase': Method(self._reserveCoinPurchase, middleware),
            'getCoinPurchaseHistory': Method(self._getCoinPurchaseHistory, middleware),
            'getCoinUseAndRefundHistory': Method(self._getCoinUseAndRefundHistory, middleware),
        }

    async def getTotalCoinBalance(self, ctx, request):
        """
        Args:
            ctx: FContext
            request: GetTotalCoinBalanceRequest
        """
        return await self._methods['getTotalCoinBalance']([ctx, request])

    async def _getTotalCoinBalance(self, ctx, request):
        memory_buffer = TMemoryOutputBuffer(self._transport.get_request_size_limit())
        oprot = self._protocol_factory.get_protocol(memory_buffer)
        oprot.write_request_headers(ctx)
        oprot.writeMessageBegin('getTotalCoinBalance', TMessageType.CALL, 0)
        args = getTotalCoinBalance_args()
        args.request = request
        args.write(oprot)
        oprot.writeMessageEnd()
        response_transport = await self._transport.request(ctx, memory_buffer.getvalue())

        iprot = self._protocol_factory.get_protocol(response_transport)
        iprot.read_response_headers(ctx)
        _, mtype, _ = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            if x.type == TApplicationExceptionType.RESPONSE_TOO_LARGE:
                raise TTransportException(type=TTransportExceptionType.RESPONSE_TOO_LARGE, message=x.message)
            raise x
        result = getTotalCoinBalance_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        if result.success is not None:
            return result.success
        raise TApplicationException(TApplicationExceptionType.MISSING_RESULT, "getTotalCoinBalance failed: unknown result")

    async def getCoinProducts(self, ctx, request):
        """
        Args:
            ctx: FContext
            request: GetCoinProductsRequest
        """
        return await self._methods['getCoinProducts']([ctx, request])

    async def _getCoinProducts(self, ctx, request):
        memory_buffer = TMemoryOutputBuffer(self._transport.get_request_size_limit())
        oprot = self._protocol_factory.get_protocol(memory_buffer)
        oprot.write_request_headers(ctx)
        oprot.writeMessageBegin('getCoinProducts', TMessageType.CALL, 0)
        args = getCoinProducts_args()
        args.request = request
        args.write(oprot)
        oprot.writeMessageEnd()
        response_transport = await self._transport.request(ctx, memory_buffer.getvalue())

        iprot = self._protocol_factory.get_protocol(response_transport)
        iprot.read_response_headers(ctx)
        _, mtype, _ = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            if x.type == TApplicationExceptionType.RESPONSE_TOO_LARGE:
                raise TTransportException(type=TTransportExceptionType.RESPONSE_TOO_LARGE, message=x.message)
            raise x
        result = getCoinProducts_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        if result.success is not None:
            return result.success
        raise TApplicationException(TApplicationExceptionType.MISSING_RESULT, "getCoinProducts failed: unknown result")

    async def reserveCoinPurchase(self, ctx, request):
        """
        Args:
            ctx: FContext
            request: CoinPurchaseReservation
        """
        return await self._methods['reserveCoinPurchase']([ctx, request])

    async def _reserveCoinPurchase(self, ctx, request):
        memory_buffer = TMemoryOutputBuffer(self._transport.get_request_size_limit())
        oprot = self._protocol_factory.get_protocol(memory_buffer)
        oprot.write_request_headers(ctx)
        oprot.writeMessageBegin('reserveCoinPurchase', TMessageType.CALL, 0)
        args = reserveCoinPurchase_args()
        args.request = request
        args.write(oprot)
        oprot.writeMessageEnd()
        response_transport = await self._transport.request(ctx, memory_buffer.getvalue())

        iprot = self._protocol_factory.get_protocol(response_transport)
        iprot.read_response_headers(ctx)
        _, mtype, _ = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            if x.type == TApplicationExceptionType.RESPONSE_TOO_LARGE:
                raise TTransportException(type=TTransportExceptionType.RESPONSE_TOO_LARGE, message=x.message)
            raise x
        result = reserveCoinPurchase_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        if result.success is not None:
            return result.success
        raise TApplicationException(TApplicationExceptionType.MISSING_RESULT, "reserveCoinPurchase failed: unknown result")

    async def getCoinPurchaseHistory(self, ctx, request):
        """
        Args:
            ctx: FContext
            request: GetCoinHistoryRequest
        """
        return await self._methods['getCoinPurchaseHistory']([ctx, request])

    async def _getCoinPurchaseHistory(self, ctx, request):
        memory_buffer = TMemoryOutputBuffer(self._transport.get_request_size_limit())
        oprot = self._protocol_factory.get_protocol(memory_buffer)
        oprot.write_request_headers(ctx)
        oprot.writeMessageBegin('getCoinPurchaseHistory', TMessageType.CALL, 0)
        args = getCoinPurchaseHistory_args()
        args.request = request
        args.write(oprot)
        oprot.writeMessageEnd()
        response_transport = await self._transport.request(ctx, memory_buffer.getvalue())

        iprot = self._protocol_factory.get_protocol(response_transport)
        iprot.read_response_headers(ctx)
        _, mtype, _ = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            if x.type == TApplicationExceptionType.RESPONSE_TOO_LARGE:
                raise TTransportException(type=TTransportExceptionType.RESPONSE_TOO_LARGE, message=x.message)
            raise x
        result = getCoinPurchaseHistory_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        if result.success is not None:
            return result.success
        raise TApplicationException(TApplicationExceptionType.MISSING_RESULT, "getCoinPurchaseHistory failed: unknown result")

    async def getCoinUseAndRefundHistory(self, ctx, request):
        """
        Args:
            ctx: FContext
            request: GetCoinHistoryRequest
        """
        return await self._methods['getCoinUseAndRefundHistory']([ctx, request])

    async def _getCoinUseAndRefundHistory(self, ctx, request):
        memory_buffer = TMemoryOutputBuffer(self._transport.get_request_size_limit())
        oprot = self._protocol_factory.get_protocol(memory_buffer)
        oprot.write_request_headers(ctx)
        oprot.writeMessageBegin('getCoinUseAndRefundHistory', TMessageType.CALL, 0)
        args = getCoinUseAndRefundHistory_args()
        args.request = request
        args.write(oprot)
        oprot.writeMessageEnd()
        response_transport = await self._transport.request(ctx, memory_buffer.getvalue())

        iprot = self._protocol_factory.get_protocol(response_transport)
        iprot.read_response_headers(ctx)
        _, mtype, _ = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            if x.type == TApplicationExceptionType.RESPONSE_TOO_LARGE:
                raise TTransportException(type=TTransportExceptionType.RESPONSE_TOO_LARGE, message=x.message)
            raise x
        result = getCoinUseAndRefundHistory_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        if result.success is not None:
            return result.success
        raise TApplicationException(TApplicationExceptionType.MISSING_RESULT, "getCoinUseAndRefundHistory failed: unknown result")


class Processor(FBaseProcessor):

    def __init__(self, handler, middleware=None):
        """
        Create a new Processor.

        Args:
            handler: Iface
        """
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]

        super(Processor, self).__init__()
        self.add_to_processor_map('getTotalCoinBalance', _getTotalCoinBalance(Method(handler.getTotalCoinBalance, middleware), self.get_write_lock()))
        self.add_to_processor_map('getCoinProducts', _getCoinProducts(Method(handler.getCoinProducts, middleware), self.get_write_lock()))
        self.add_to_processor_map('reserveCoinPurchase', _reserveCoinPurchase(Method(handler.reserveCoinPurchase, middleware), self.get_write_lock()))
        self.add_to_processor_map('getCoinPurchaseHistory', _getCoinPurchaseHistory(Method(handler.getCoinPurchaseHistory, middleware), self.get_write_lock()))
        self.add_to_processor_map('getCoinUseAndRefundHistory', _getCoinUseAndRefundHistory(Method(handler.getCoinUseAndRefundHistory, middleware), self.get_write_lock()))


class _getTotalCoinBalance(FProcessorFunction):

    def __init__(self, handler, lock):
        super(_getTotalCoinBalance, self).__init__(handler, lock)

    async def process(self, ctx, iprot, oprot):
        args = getTotalCoinBalance_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getTotalCoinBalance_result()
        try:
            ret = self._handler([ctx, args.request])
            if inspect.iscoroutine(ret):
                ret = await ret
            result.success = ret
        except TApplicationException as ex:
            async with self._lock:
                _write_application_exception(ctx, oprot, "getTotalCoinBalance", exception=ex)
                return
        except CoinException as e:
            result.e = e
        except Exception as e:
            async with self._lock:
                _write_application_exception(ctx, oprot, "getTotalCoinBalance", ex_code=TApplicationExceptionType.INTERNAL_ERROR, message=str(e))
            raise
        async with self._lock:
            try:
                oprot.write_response_headers(ctx)
                oprot.writeMessageBegin('getTotalCoinBalance', TMessageType.REPLY, 0)
                result.write(oprot)
                oprot.writeMessageEnd()
                oprot.get_transport().flush()
            except TTransportException as e:
                # catch a request too large error because the TMemoryOutputBuffer always throws that if too much data is written
                if e.type == TTransportExceptionType.REQUEST_TOO_LARGE:
                    raise _write_application_exception(ctx, oprot, "getTotalCoinBalance", ex_code=TApplicationExceptionType.RESPONSE_TOO_LARGE, message=e.message)
                else:
                    raise e


class _getCoinProducts(FProcessorFunction):

    def __init__(self, handler, lock):
        super(_getCoinProducts, self).__init__(handler, lock)

    async def process(self, ctx, iprot, oprot):
        args = getCoinProducts_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getCoinProducts_result()
        try:
            ret = self._handler([ctx, args.request])
            if inspect.iscoroutine(ret):
                ret = await ret
            result.success = ret
        except TApplicationException as ex:
            async with self._lock:
                _write_application_exception(ctx, oprot, "getCoinProducts", exception=ex)
                return
        except CoinException as e:
            result.e = e
        except Exception as e:
            async with self._lock:
                _write_application_exception(ctx, oprot, "getCoinProducts", ex_code=TApplicationExceptionType.INTERNAL_ERROR, message=str(e))
            raise
        async with self._lock:
            try:
                oprot.write_response_headers(ctx)
                oprot.writeMessageBegin('getCoinProducts', TMessageType.REPLY, 0)
                result.write(oprot)
                oprot.writeMessageEnd()
                oprot.get_transport().flush()
            except TTransportException as e:
                # catch a request too large error because the TMemoryOutputBuffer always throws that if too much data is written
                if e.type == TTransportExceptionType.REQUEST_TOO_LARGE:
                    raise _write_application_exception(ctx, oprot, "getCoinProducts", ex_code=TApplicationExceptionType.RESPONSE_TOO_LARGE, message=e.message)
                else:
                    raise e


class _reserveCoinPurchase(FProcessorFunction):

    def __init__(self, handler, lock):
        super(_reserveCoinPurchase, self).__init__(handler, lock)

    async def process(self, ctx, iprot, oprot):
        args = reserveCoinPurchase_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = reserveCoinPurchase_result()
        try:
            ret = self._handler([ctx, args.request])
            if inspect.iscoroutine(ret):
                ret = await ret
            result.success = ret
        except TApplicationException as ex:
            async with self._lock:
                _write_application_exception(ctx, oprot, "reserveCoinPurchase", exception=ex)
                return
        except CoinException as e:
            result.e = e
        except Exception as e:
            async with self._lock:
                _write_application_exception(ctx, oprot, "reserveCoinPurchase", ex_code=TApplicationExceptionType.INTERNAL_ERROR, message=str(e))
            raise
        async with self._lock:
            try:
                oprot.write_response_headers(ctx)
                oprot.writeMessageBegin('reserveCoinPurchase', TMessageType.REPLY, 0)
                result.write(oprot)
                oprot.writeMessageEnd()
                oprot.get_transport().flush()
            except TTransportException as e:
                # catch a request too large error because the TMemoryOutputBuffer always throws that if too much data is written
                if e.type == TTransportExceptionType.REQUEST_TOO_LARGE:
                    raise _write_application_exception(ctx, oprot, "reserveCoinPurchase", ex_code=TApplicationExceptionType.RESPONSE_TOO_LARGE, message=e.message)
                else:
                    raise e


class _getCoinPurchaseHistory(FProcessorFunction):

    def __init__(self, handler, lock):
        super(_getCoinPurchaseHistory, self).__init__(handler, lock)

    async def process(self, ctx, iprot, oprot):
        args = getCoinPurchaseHistory_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getCoinPurchaseHistory_result()
        try:
            ret = self._handler([ctx, args.request])
            if inspect.iscoroutine(ret):
                ret = await ret
            result.success = ret
        except TApplicationException as ex:
            async with self._lock:
                _write_application_exception(ctx, oprot, "getCoinPurchaseHistory", exception=ex)
                return
        except CoinException as e:
            result.e = e
        except Exception as e:
            async with self._lock:
                _write_application_exception(ctx, oprot, "getCoinPurchaseHistory", ex_code=TApplicationExceptionType.INTERNAL_ERROR, message=str(e))
            raise
        async with self._lock:
            try:
                oprot.write_response_headers(ctx)
                oprot.writeMessageBegin('getCoinPurchaseHistory', TMessageType.REPLY, 0)
                result.write(oprot)
                oprot.writeMessageEnd()
                oprot.get_transport().flush()
            except TTransportException as e:
                # catch a request too large error because the TMemoryOutputBuffer always throws that if too much data is written
                if e.type == TTransportExceptionType.REQUEST_TOO_LARGE:
                    raise _write_application_exception(ctx, oprot, "getCoinPurchaseHistory", ex_code=TApplicationExceptionType.RESPONSE_TOO_LARGE, message=e.message)
                else:
                    raise e


class _getCoinUseAndRefundHistory(FProcessorFunction):

    def __init__(self, handler, lock):
        super(_getCoinUseAndRefundHistory, self).__init__(handler, lock)

    async def process(self, ctx, iprot, oprot):
        args = getCoinUseAndRefundHistory_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getCoinUseAndRefundHistory_result()
        try:
            ret = self._handler([ctx, args.request])
            if inspect.iscoroutine(ret):
                ret = await ret
            result.success = ret
        except TApplicationException as ex:
            async with self._lock:
                _write_application_exception(ctx, oprot, "getCoinUseAndRefundHistory", exception=ex)
                return
        except CoinException as e:
            result.e = e
        except Exception as e:
            async with self._lock:
                _write_application_exception(ctx, oprot, "getCoinUseAndRefundHistory", ex_code=TApplicationExceptionType.INTERNAL_ERROR, message=str(e))
            raise
        async with self._lock:
            try:
                oprot.write_response_headers(ctx)
                oprot.writeMessageBegin('getCoinUseAndRefundHistory', TMessageType.REPLY, 0)
                result.write(oprot)
                oprot.writeMessageEnd()
                oprot.get_transport().flush()
            except TTransportException as e:
                # catch a request too large error because the TMemoryOutputBuffer always throws that if too much data is written
                if e.type == TTransportExceptionType.REQUEST_TOO_LARGE:
                    raise _write_application_exception(ctx, oprot, "getCoinUseAndRefundHistory", ex_code=TApplicationExceptionType.RESPONSE_TOO_LARGE, message=e.message)
                else:
                    raise e


def _write_application_exception(ctx, oprot, method, ex_code=None, message=None, exception=None):
    if exception is not None:
        x = exception
    else:
        x = TApplicationException(type=ex_code, message=message)
    oprot.write_response_headers(ctx)
    oprot.writeMessageBegin(method, TMessageType.EXCEPTION, 0)
    x.write(oprot)
    oprot.writeMessageEnd()
    oprot.get_transport().flush()
    return x

class getTotalCoinBalance_args(object):
    """
    Attributes:
     - request
    """
    def __init__(self, request=None):
        self.request = request

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.request = GetTotalCoinBalanceRequest()
                    self.request.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('getTotalCoinBalance_args')
        if self.request is not None:
            oprot.writeFieldBegin('request', TType.STRUCT, 1)
            self.request.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.request))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class getTotalCoinBalance_result(object):
    """
    Attributes:
     - success
     - e
    """
    def __init__(self, success=None, e=None):
        self.success = success
        self.e = e

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = GetTotalCoinBalanceResponse()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.e = CoinException()
                    self.e.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('getTotalCoinBalance_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.e is not None:
            oprot.writeFieldBegin('e', TType.STRUCT, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.success))
        value = (value * 31) ^ hash(make_hashable(self.e))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class getCoinProducts_args(object):
    """
    Attributes:
     - request
    """
    def __init__(self, request=None):
        self.request = request

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.request = GetCoinProductsRequest()
                    self.request.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('getCoinProducts_args')
        if self.request is not None:
            oprot.writeFieldBegin('request', TType.STRUCT, 1)
            self.request.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.request))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class getCoinProducts_result(object):
    """
    Attributes:
     - success
     - e
    """
    def __init__(self, success=None, e=None):
        self.success = success
        self.e = e

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = GetCoinProductsResponse()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.e = CoinException()
                    self.e.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('getCoinProducts_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.e is not None:
            oprot.writeFieldBegin('e', TType.STRUCT, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.success))
        value = (value * 31) ^ hash(make_hashable(self.e))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class reserveCoinPurchase_args(object):
    """
    Attributes:
     - request
    """
    def __init__(self, request=None):
        self.request = request

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.request = CoinPurchaseReservation()
                    self.request.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('reserveCoinPurchase_args')
        if self.request is not None:
            oprot.writeFieldBegin('request', TType.STRUCT, 1)
            self.request.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.request))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class reserveCoinPurchase_result(object):
    """
    Attributes:
     - success
     - e
    """
    def __init__(self, success=None, e=None):
        self.success = success
        self.e = e

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = PaymentReservationResult()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.e = CoinException()
                    self.e.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('reserveCoinPurchase_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.e is not None:
            oprot.writeFieldBegin('e', TType.STRUCT, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.success))
        value = (value * 31) ^ hash(make_hashable(self.e))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class getCoinPurchaseHistory_args(object):
    """
    Attributes:
     - request
    """
    def __init__(self, request=None):
        self.request = request

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.request = GetCoinHistoryRequest()
                    self.request.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('getCoinPurchaseHistory_args')
        if self.request is not None:
            oprot.writeFieldBegin('request', TType.STRUCT, 1)
            self.request.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.request))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class getCoinPurchaseHistory_result(object):
    """
    Attributes:
     - success
     - e
    """
    def __init__(self, success=None, e=None):
        self.success = success
        self.e = e

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = GetCoinHistoryResponse()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.e = CoinException()
                    self.e.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('getCoinPurchaseHistory_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.e is not None:
            oprot.writeFieldBegin('e', TType.STRUCT, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.success))
        value = (value * 31) ^ hash(make_hashable(self.e))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class getCoinUseAndRefundHistory_args(object):
    """
    Attributes:
     - request
    """
    def __init__(self, request=None):
        self.request = request

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.request = GetCoinHistoryRequest()
                    self.request.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('getCoinUseAndRefundHistory_args')
        if self.request is not None:
            oprot.writeFieldBegin('request', TType.STRUCT, 1)
            self.request.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.request))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class getCoinUseAndRefundHistory_result(object):
    """
    Attributes:
     - success
     - e
    """
    def __init__(self, success=None, e=None):
        self.success = success
        self.e = e

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = GetCoinHistoryResponse()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.e = CoinException()
                    self.e.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('getCoinUseAndRefundHistory_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.e is not None:
            oprot.writeFieldBegin('e', TType.STRUCT, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.success))
        value = (value * 31) ^ hash(make_hashable(self.e))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

