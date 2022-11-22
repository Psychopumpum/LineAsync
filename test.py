#!usr/bin/python
# -*- coding: utf-8 -*-
import nest_asyncio
nest_asyncio.apply()
import asyncio, time, traceback, sys, os, httpx
from LineAsync import *
import axolotl_curve25519 as curve
from concurrent.futures import ThreadPoolExecutor

#client = Client("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI2NzNlY2Q2Mi00ZDEwLTQ5OTEtOGE2Zi00NzgwZGNiNTc2ZTEiLCJhdWQiOiJMSU5FIiwiaWF0IjoxNjY4OTI1MTIxLCJleHAiOjE2Njk1Mjk5MjEsInNjcCI6IkxJTkVfQ09SRSIsInJ0aWQiOiJjOGI5MmQ0My03NmZiLTQ3NmEtOTJkMC05ZTI2MTU4YTU4YjAiLCJyZXhwIjoxNzAwNDYxMTIxLCJ2ZXIiOiIzLjEiLCJhaWQiOiJ1MjQwYWY4MzVlNGMwMTk5MWNlN2ViNjk0ZWE2NTJjOGYiLCJsc2lkIjoiMzdmZjk2ZjItMzM1MC00YTI5LTljOWQtMzczNGFlZjYwYWM1IiwiZGlkIjoiTk9ORSIsImN0eXBlIjoiQ0hST01FT1MiLCJjbW9kZSI6IlNFQ09OREFSWSIsImNpZCI6IjAzMDAwMDAwMDAifQ.iO4dFntIkPULbPvDufmCRkdBw4YfyqVYquG_O_HNZRg", certificate = "08dfef34d4d6fc8e7d138d683c229a8e76ffe4b40c6f459f43224053fbf09344", appType = "CHROMEOS")
client = Client("ua4d14b263eaaf5c3f8a28c23fbc648f5:aWF0OiAxNjM4ODM1NzA0MzEzCg==..KFKhajdqfVXUipKV3OHX6UQVWQk=", appType = "IOS")
poll = ThreadPoolExecutor(30)
data = {}


def run(corofn, *args):
    loop = asyncio.new_event_loop()
    try:
        coro = corofn(*args)
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    finally:
        loop.close()

async def download(to, msg):
    if msg.contentType == 1:
        if to in data and data[to].get(msg._from):
            if data[to][msg._from]['state']:
                task = []
                url = f"{client.server.OBJECT_STORAGE_SERVER_HOST}/talk/m/download.nhn?oid={msg.id}"
                if url not in data[to][msg._from]["urls"]:
                    data[to][msg._from]["urls"].append(url)
                    data[to][msg._from]["types"].append("PHOTO")
                if len(data[to][msg._from]["urls"]) == data[to][msg._from]["amount"]:
                    for no, url in enumerate(zip(data[to][msg._from]["urls"], data[to][msg._from]["types"]), start = 1):
                        name = url[0].split('oid=')[1]
                        ext = ".mp4" if url[1] == "VIDEO" else ".jpg"
                        task.append(asyncio.ensure_future(client.downloadObjectMsg(url[0], "path", saveAs = f"downloads/{name}{ext}")))
                    await client.sendMessage(to, "Progress download has started...")
                    s_d = time.time()
                    datas = await asyncio.gather(*task)
                    tasks = []
                    for oid in datas:
                        if oid.endswith(".mp4"):
                            tasks.append(asyncio.ensure_future(client.uploadObjectHome(oid, "video", returnAs = "headers", updatePost = True)))
                        else:
                            tasks.append(asyncio.ensure_future(client.uploadObjectHome(oid, "image", returnAs = "headers", updatePost = True)))
                    task.clear()
                    await client.sendMessage(to, f"Download completes\n\t• Took: {round(time.time()-s_d, 2)} sec.\n\nCreating a task upload file in progress.")
                    s_u = time.time()
                    datas = await asyncio.gather(*tasks)
                    for oids in tasks:
                        result = oids.result()
                        if result.get("x-obs-content-type").startswith("image"):
                            data[to][msg._from]['media'].append({
                                "type": "PHOTO",
                                "objectId": result.get("x-obs-oid")
                            })
                        else:
                            data[to][msg._from]['media'].append({
                                "type": "VIDEO",
                                "objectId": result.get("x-obs-oid")
                            })
                    await client.sendMessage(to, f"Upload file complete\n\t• Took: {round(time.time()-s_u, 2)} sec.")
                if len(data[to][msg._from]["media"]) >= data[to][msg._from]["amount"]:
                    a = await client.createPost(to, medias = data[to][msg._from]["media"])
                    del data[to][msg._from]
    elif msg.contentType == 2:
        if to in data and data[to].get(msg._from):
            if data[to][msg._from]['state']:
                task = []
                url = f"{client.server.OBJECT_STORAGE_SERVER_HOST}/talk/m/download.nhn?oid={msg.id}"
                if url not in data[to][msg._from]["urls"]:
                    data[to][msg._from]["urls"].append(url)
                    data[to][msg._from]["types"].append("VIDEO")
                if len(data[to][msg._from]["urls"]) == data[to][msg._from]["amount"]:
                    for no, url in enumerate(zip(data[to][msg._from]["urls"], data[to][msg._from]["types"]), start = 1):
                        name = url[0].split('oid=')[1]
                        ext = ".mp4" if url[1] == "VIDEO" else ".jpg"
                        task.append(asyncio.ensure_future(client.downloadObjectMsg(url[0], "path", saveAs = f"downloads/{name}{ext}")))
                    await client.sendMessage(to, "Progress download has started...")
                    s_d = time.time()
                    datas = await asyncio.gather(*task)
                    tasks = []
                    for oid in datas:
                        if oid.endswith(".mp4"):
                            tasks.append(asyncio.ensure_future(client.uploadObjectHome(oid, "video", returnAs = "headers", updatePost = True)))
                        else:
                            tasks.append(asyncio.ensure_future(client.uploadObjectHome(oid, "image", returnAs = "headers", updatePost = True)))
                    task.clear()
                    await client.sendMessage(to, f"Download completes\n\t• Took: {round(time.time()-s_d, 2)} sec.\n\nCreating a task upload file in progress.")
                    s_u = time.time()
                    datas = await asyncio.gather(*tasks)
                    for oids in tasks:
                        result = oids.result()
                        if result.get("x-obs-content-type").startswith("video"):
                            data[to][msg._from]['media'].append({
                                "type": "VIDEO",
                                "objectId": result.get("x-obs-oid")
                            })
                        else:
                            data[to][msg._from]['media'].append({
                                "type": "PHOTO",
                                "objectId": result.get("x-obs-oid")
                            })
                    await client.sendMessage(to, f"Upload file complete\n\t• Took: {round(time.time()-s_u, 2)} sec.")
                if len(data[to][msg._from]["media"]) >= data[to][msg._from]["amount"]:
                    a = await client.createPost(to, medias = data[to][msg._from]["media"])
                    del data[to][msg._from]

async def main(op):
    try:
        if op.type == 26:
            msg = op.message
            text = str(msg.text)
            to = msg._from if msg.toType == 0 and msg._from != client.profile.mid else msg.to
            author = ["u240af835e4c01991ce7eb694ea652c8f"]
            if not msg.contentType:
                if text.lower() == "speed":
                    s = time.time()
                    await client.getProfile()
                    await client.sendMessage(to, f"{round((time.time()-s)*1000, 2)} ms.")
                elif text.lower().startswith("createnote"):
                    cmd = text[len("createnote "):]
                    if not cmd.isdigit():
                        return await client.sendMessage(to, "Amount of total must be a digits.")
                    if to not in data:
                        data[to] = {}
                    if msg._from not in data[to]:
                        data[to][msg._from] = {
                            "state": True,
                            "amount": int(cmd),
                            "media": [],
                            "urls": [],
                            "types": [],
                            "oid": []
                        }
                    return await client.sendMessage(to, "Sent a video or picture...")
                elif text.lower().startswith('cname') and msg._from in author:
                    cmd = text[len("cname "):]
                    return await client.updateProfileAttributes("DISPLAY_NAME", cmd)
                elif text.lower() == "me":
                    await client.sendMessage(to, "", {"mid": msg._from}, contentType = 13)
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
            elif msg.contentType == 1 or msg.contentType == 2:
                with ThreadPoolExecutor(30) as pools:
                    r = pools.submit(run, download, to, msg)
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