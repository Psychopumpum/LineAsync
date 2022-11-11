#!usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
from LineAsync import *

client = Client(appType = "WEAROS")
"""
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5OTI5MTk5MC02MjI4LTQ1MWQtOGU4OS1kYmUwMDMyZDg1ZGMiLCJhdWQiOiJMSU5FIiwiaWF0IjoxNjY3MDY0NDUxLCJleHAiOjE2Njc2NjkyNTEsInNjcCI6IkxJTkVfQ09SRSIsInJ0aWQiOiI3ZWVhZDlmZi03ODY1LTQwMDktYTdjZi03N2ZjMTIzMjg4MDgiLCJyZXhwIjoxNjk4NjAwNDUxLCJ2ZXIiOiIzLjEiLCJhaWQiOiJ1MjQwYWY4MzVlNGMwMTk5MWNlN2ViNjk0ZWE2NTJjOGYiLCJsc2lkIjoiZmMzNWEzOTQtMTUwYi00ZTZiLWEwYTMtMGZmNjlmNTJhNzgyIiwiZGlkIjoiTk9ORSIsImN0eXBlIjoiQU5EUk9JRFNFQ09OREFSWSIsImNtb2RlIjoiU0VDT05EQVJZIiwiY2lkIjoiMDkwMDAwMDAwMCJ9.3yT6I5aK2cA9y3YE9dMQ3tJXHoYIBcEwyeDyE_U4_Bc",
    certificate = "32148f1f83cceff20f9629c0d000a16dc582cc42b01f6869facc01b78a17d93b",
    appType = "ANDROIDSECONDARY"
)"""

async def main(op):
    try:
        print(op.type, OpType._VALUES_TO_NAMES[op.type])
    except TalkException as e:
        print(f"an error occured:\n\t• Code: {e.code}\n\t• Reason: {e.reason}\n\t• paramaterMap: {e.parameterMap}")

async def run():
    try:
        while 1:
            ops = await client.poll.fetchOps(100)
            if not ops:
                return []
            for op in ops:
                if op.revision == -1 and op.param2 != None:
                    client.globalRev = int(op.param2.split("\x1e")[0])
                if op.revision == -1 and op.param1 != None:
                    client.individualRev = int(op.param1.split("\x1e")[0])
                client.setRevision(op.revision)
                await main(op)
    except KeyboardInterrupt:
        sys.exit("Keyboard Interrupted.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run())