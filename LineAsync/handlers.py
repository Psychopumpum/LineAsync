from typing import Callable
from .filters import Filter
import LineAsync, inspect

from collections import OrderedDict

class BaseClient:

    locks_list = []
    groups = OrderedDict()

    def add_handler(self, handler, type: int):
        async def fn():
            for lock in self.locks_list:
                await lock.acquire()

            try:
                if type not in self.groups:
                    self.groups[type] = []
                    self.groups = OrderedDict(sorted(self.groups.items()))

                self.groups[type].append(handler)
            finally:
                for lock in self.locks_list:
                    lock.release()

        asyncio.get_event_loop().create_task(fn())

class Handler:

    def __init__(self, callback: Callable, filters: Filter = None):
        self.callback = callback
        self.filters = filters

    async def check(self, client, message):
        if callable(self.filters):
            if inspect.iscoroutinefunction(self.filters.__call__):
                return await self.filters(client, message)
            else:
                return await client._loop.run_in_executor(
                    client.executor,
                    self.filters,
                    client, message
                )

        return True

class MessageHandler(Handler):

    def __init__(self, callback: Callable, filters: Filter = None):
        super().__init__(callback, filters)

class HookMessage(BaseClient):

    def on_message(self = None, filters = None, type: int = 0) -> Callable:

        def decorator(func: Callable) -> Callable:

            if isinstance(self, LineAsync.Client):
                self.add_handler(type, MessageHandler(func, filters).callback, filters)

            elif isinstance(self, Filter) or self is None:

                func.line_plugin = (MessageHandler(func, filters), type)
                try:
                    return func.line_plugin
                except AttributeError:
                    return func

            return func

        return decorator

class Methods(HookMessage):
    pass