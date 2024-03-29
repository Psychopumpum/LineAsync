# Copyright 2017 Workiva
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

import asyncio
import async_timeout

from thrift.protocol.TProtocol import TProtocolException
from thrift.transport.TTransport import TMemoryBuffer
from thrift.transport.TTransport import TTransportException

from frugal.aio.transport import FTransportBase
from frugal.context import _OPID_HEADER
from frugal.exceptions import TTransportExceptionType
from frugal.context import FContext
from frugal.util.headers import _Headers


logger = logging.getLogger(__name__)

_EMPTY_MESSAGE = []


class FAsyncTransport(FTransportBase):
    """
     FAsyncTransport is an extension of FTransportBase that asynchronous
     frameworks can implement. Implementations need only implement flush to
     send request data and call handle_response when asynchronous responses
     are received.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._futures = {}
        self._futures_lock = asyncio.Lock()

    async def oneway(self, context: FContext, payload):
        self._preflight_request_check(payload)
        try:
            with async_timeout.timeout(context.timeout / 1000):
                await self.flush(payload)
        except asyncio.TimeoutError:
            raise TTransportException(
                type=TTransportExceptionType.TIMED_OUT,
                message='request timed out'
            ) from None

    async def request(self, context: FContext, payload):
        self._preflight_request_check(payload)
        op_id = str(context._get_op_id())
        future = asyncio.Future()
        async with self._futures_lock:
            if op_id in self._futures:
                raise TTransportException(
                    type=TTransportExceptionType.UNKNOWN,
                    message="request already in flight for context"
                )
            self._futures[op_id] = future

        try:
            with async_timeout.timeout(context.timeout / 1000):
                await self.flush_op(op_id, payload)
                resp = await future
                if resp == _EMPTY_MESSAGE:
                    raise TTransportException(
                        type=TTransportExceptionType.SERVICE_NOT_AVAILABLE,
                        message="request: service not available"
                    )

                return TMemoryBuffer(resp)
        except asyncio.TimeoutError:
            raise TTransportException(
                type=TTransportExceptionType.TIMED_OUT,
                message='request timed out'
            ) from None
        finally:
            async with self._futures_lock:
                del self._futures[op_id]

    async def flush(self, payload):
        """Flush the payload to the server."""
        raise NotImplementedError('You must override this')

    async def flush_op(self, op_id, payload):
        """Flush the payload to the server."""
        await self.flush(payload)

    async def handle_response(self, message):
        """
        Complete the future associated with the data frame.

        Args:
            frame: The response frame
        """
        if not message.data:
            logger.debug("Received empty message")
            op_id = message.subject[message.subject.rindex(".") + 1:]
            await self.handle_empty_response(op_id)
            return
        frame = message.data[4:]
        headers = _Headers.decode_from_frame(frame)
        op_id = headers.get(_OPID_HEADER, None)

        if not op_id:
            raise TProtocolException(message="Frame missing op_id")

        await self._handle_op_response(op_id, frame)

    async def _handle_op_response(self, op_id, frame):

        async with self._futures_lock:
            future = self._futures.get(op_id, None)
            if not future:
                return

            future.set_result(frame)

    async def handle_empty_response(self, op_id):
        async with self._futures_lock:
            future = self._futures.get(op_id, None)
            if not future:
                return

            future.set_result(_EMPTY_MESSAGE)
