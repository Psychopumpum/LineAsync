#!usr/bin/python
# -*- coding: utf-8 -*-
import asyncio, time, traceback, sys, os
from LineAsync import *
import axolotl_curve25519 as curve
from concurrent.futures import ThreadPoolExecutor

#client = Client("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI2NzNlY2Q2Mi00ZDEwLTQ5OTEtOGE2Zi00NzgwZGNiNTc2ZTEiLCJhdWQiOiJMSU5FIiwiaWF0IjoxNjY4OTI1MTIxLCJleHAiOjE2Njk1Mjk5MjEsInNjcCI6IkxJTkVfQ09SRSIsInJ0aWQiOiJjOGI5MmQ0My03NmZiLTQ3NmEtOTJkMC05ZTI2MTU4YTU4YjAiLCJyZXhwIjoxNzAwNDYxMTIxLCJ2ZXIiOiIzLjEiLCJhaWQiOiJ1MjQwYWY4MzVlNGMwMTk5MWNlN2ViNjk0ZWE2NTJjOGYiLCJsc2lkIjoiMzdmZjk2ZjItMzM1MC00YTI5LTljOWQtMzczNGFlZjYwYWM1IiwiZGlkIjoiTk9ORSIsImN0eXBlIjoiQ0hST01FT1MiLCJjbW9kZSI6IlNFQ09OREFSWSIsImNpZCI6IjAzMDAwMDAwMDAifQ.iO4dFntIkPULbPvDufmCRkdBw4YfyqVYquG_O_HNZRg", certificate = "08dfef34d4d6fc8e7d138d683c229a8e76ffe4b40c6f459f43224053fbf09344", appType = "CHROMEOS")
client = Client("ua4d14b263eaaf5c3f8a28c23fbc648f5:aWF0OiAxNjM4ODM1NzA0MzEzCg==..KFKhajdqfVXUipKV3OHX6UQVWQk=", appType = "IOS")
poll = ThreadPoolExecutor(30)

async def main(op):
    try:
        if op.type == 26:
            msg = op.message
            text = str(msg.text)
            to = msg._from if msg.toType == 0 and msg._from != self.profile.mid else msg.to
            if text.lower() == "speed":
                s = time.time()
                await client.getProfile()
                await client.sendMessage(to, f"{round((time.time()-s)*1000, 2)} ms.")
            elif text.lower() == "restart":
                arr = sys.executable
                os.system('clear')
                await client.sendMessage(to, "Restarting...")
                os.execl(arr, arr, *sys.argv)
            elif text.lower() == "grouplist":
                ret = "GroupList:\n"
                numb = 49
                for i in range(0, len(client.groupList), numb):
                    for no, chat in enumerate(client.groupList[i:i+numb], i+1):
                        if numb <= 49:
                            numb += 1
                        if no == len(client.groupList):ret += f"{no}. {chat.chatName}"
                        else:ret += f"{no}. {chat.chatName}\n"
                    if ret.endswith("\n"):ret = ret[:-1]
                    await client.sendMessage(to, ret)
                    ret = ''
    except Exception:
        traceback.print_exc()

async def fetch():
    try:
        while not client.poll.fetch_event.is_set():
            ops = await client.poll.fetchOps(100)
            for op in ops:
                if op.revision == -1 and op.param2 != None:
                    client.poll.globalRev = int(op.param2.split("\x1e")[0])
                if op.revision == -1 and op.param1 != None:
                    client.poll.individualRev = int(op.param1.split("\x1e")[0])
                await client.poll.setRevision(op.revision)
                await asyncio.create_task(main(op))
    except EOFError:
        pass
    except Exception:
        traceback.print_exc()
    except KeyboardInterrupt:
        client._loop.stop()
        sys.exit("Keyboad interrupt.")

if __name__ == "__main__":
    client._loop.run_until_complete(fetch())