# -*- coding: utf-8 -*-
from .filters import Filter
from .auth import Connection
from types import LambdaType
from frugal.context import FContext
from LineFrugal import FTalkServiceClient, ttypes
import concurrent.futures

import asyncio, traceback, inspect, functools, signal, sys

class OEPoll(Connection):

    def __init__(self, client, loop = None):
        self.cl_ = client
        Connection.__init__(self, self.cl_.server.TALK_SERVER_HOST + "/P4", FTalkServiceClient, 4000, request = "httplib2")
        self.cl_.server.pollHeaders.update({
            "X-Line-Access": self.cl_.accessToken
        })
        self.transport.setCustomHeaders(self.cl_.server.pollHeaders)
        self.revision      = -1
        self.globalRev     = 0
        self.individualRev = 0
        self.loop          = loop if loop else self.cl_._loop
        self.fetch_event   = asyncio.Event()
        self.plug_handler  = {}

    async def _fetchOps(self, count: int):
        return await self.call("fetchOps", self.revision, count, self.globalRev, self.individualRev)

    async def fetchOps(self, count: int):
        try:
            ops = await self._fetchOps(count)
        except KeyboardInterrupt:
            sys.exit("Keyboard Interrupted.")
        except EOFError:
            return []
        except Exception:
            traceback.print_exc()
        if not ops:return []
        return ops

    async def setRevision(self, rev):
        self.revision = max(self.revision, rev)

    def run(self):
        self.cl_._loop.run_until_complete(self.start())

    async def execute_handler(self, coro, *args, **kwgs):
        if inspect.isroutine(coro) or inspect.iscoroutinefunction(coro):
            coros = await coro(*args, **kwgs)
        else:
            coros = coro(*args, **kwgs)
        return coros

    def ask_exit(self, signame):
        self.cl_._loop.stop()
        sys.exit("got signal %s: exit" % signame)

    async def start(self, count: int = 100):
        while not self.fetch_event.is_set():
            try:
                ops = await self._fetchOps(count)
            except KeyboardInterrupt:
                for signame in {'SIGINT', 'SIGTERM'}:
                    self.cl_._loop.stop()
                    sys.exit(f"Got signal {getattr(signal, signame)}: Exit")
            except EOFError:
                pass
            except Exception:
                traceback.print_exc()
            if not ops:
                return []
            for op in ops:
                await self.setRevision(op.revision)
                if op.revision == -1 and op.param2 != None:
                    self.globalRev = int(op.param2.split("\x1e")[0])
                if op.revision == -1 and op.param1 != None:
                    self.individualRev = int(op.param1.split("\x1e")[0])
                print(f"[ {op.type} ]", ttypes.OpType._VALUES_TO_NAMES[op.type].replace("_", " "))
                if self.plug_handler:
                    for handler, funcs in self.plug_handler.items():
                        if handler == op.type:
                            for func in funcs:
                                for k, v in func.items():
                                    if func[k][0] and isinstance(func[k][0], Filter):
                                        if func[k][0](op.message):
                                            with concurrent.futures.ThreadPoolExecutor(5) as pool:
                                                result = await self.cl_._loop.run_in_executor(
                                                    pool, self.execute_handler, k, func[k][1], op.message
                                                )
                                                await asyncio.wait([result])
                                    elif isinstance(func[k][0], LambdaType):
                                        if func[k][0](func[k][1], op if op.type not in [25, 26] else op.message):
                                            with concurrent.futures.ThreadPoolExecutor(5) as pool:
                                                result = await self.cl_._loop.run_in_executor(
                                                    pool, self.execute_handler, k, func[k][1], op if op.type not in [25, 26] else op.message
                                                )
                                                await asyncio.wait([result])
                                    elif not func[k][0]:
                                        with concurrent.futures.ThreadPoolExecutor(5) as pool:
                                            result = await self.cl_._loop.run_in_executor(
                                                pool, self.execute_handler, k, func[k][1], op
                                            )
                                            await asyncio.wait([result])