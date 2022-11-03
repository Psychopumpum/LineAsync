# -*- coding: utf-8 -*-
from .filters import Filter
from .auth import Connection
from types import LambdaType
from frugal.context import FContext
from LineFrugal.TalkService import FTalkServiceClient
from concurrent.futures.thread import ThreadPoolExecutor

import asyncio, traceback, inspect

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
        self.loop          = loop if loop else asyncio.get_event_loop()
        self.fetch_event   = asyncio.Event(loop=self.loop)
        self.plug_handler  = {}

    async def fetchOps(self, count: int):
        return await self.call("fetchOps", self.revision, count, self.globalRev, self.individualRev)

    async def setRevision(self, rev):
        self.revision = max(self.revision, rev)

    def run(self):
        self.cl_._loop.run_until_complete(self.start())

    async def execute_handler(self, coro, *args, **kwgs):
        if inspect.isroutine(coro) or inspect.iscoroutinefunction(coro):
            return await coro(*args, **kwgs)
        return coro(*args, **kwgs)

    async def start(self, count: int = 100):
        while not self.fetch_event.is_set():
            try:
                ops = await self.fetchOps(count)
                if not ops:
                    return []
                for op in ops:
                    await self.setRevision(op.revision)
                    if op.revision == -1 and op.param2 != None:
                        self.globalRev = int(op.param2.split("\x1e")[0])
                    if op.revision == -1 and op.param1 != None:
                        self.individualRev = int(op.param1.split("\x1e")[0])
                    if self.plug_handler:
                        for handler, funcs in self.plug_handler.items():
                            if handler == op.type:
                                for func in funcs:
                                    for k, v in func.items():
                                        if func[k][0] and isinstance(func[k][0], Filter):
                                            if func[k][0](op.message):
                                                await self.execute_handler(k, func[k][1], op.message)
                                        elif isinstance(func[k][0], LambdaType):
                                            if func[k][0](func[k][1], op if op.type not in [25, 26] else op.message):
                                                await self.execute_handler(k, func[k][1], op if op.type not in [25, 26] else op.message)
                                        elif not func[k][0]:
                                            await self.execute_handler(k, func[k][1], op)
            except KeyboardInterrupt:
                raise
            except Exception:
                traceback.print_exc()