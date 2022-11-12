#!usr/bin/python
# -*- coding: utf-8 -*-
import asyncio, time
from LineAsync import *

import concurrent.futures

client = Client(
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiYjNhMWRiOC02OTYzLTRkNjAtOTk3NC0wMTYyNDY5YTJiNzYiLCJhdWQiOiJMSU5FIiwiaWF0IjoxNjY4MjQwNzk0LCJleHAiOjE2Njg4NDU1OTQsInNjcCI6IkxJTkVfQ09SRSIsInJ0aWQiOiIyMGVjMWFmNC1mZjk1LTQwYjEtOTM3Mi0yYTQ4NTU4YWI2Y2IiLCJyZXhwIjoxNjk5Nzc2Nzk0LCJ2ZXIiOiIzLjEiLCJhaWQiOiJ1MjQwYWY4MzVlNGMwMTk5MWNlN2ViNjk0ZWE2NTJjOGYiLCJsc2lkIjoiYjBiYTU5MTUtNGQyNi00MmNjLWExM2UtNTBmYjVmOWMwNjZlIiwiZGlkIjoiTk9ORSIsImN0eXBlIjoiQU5EUk9JRFNFQ09OREFSWSIsImNtb2RlIjoiU0VDT05EQVJZIiwiY2lkIjoiMDkwMDAwMDAwMCJ9.TY70WesdKerxTfXjN8LLt-Mx1hOMXZdfR-AzT-XpQMc",
    certificate = "32148f1f83cceff20f9629c0d000a16dc582cc42b01f6869facc01b78a17d93b",
    appType = "ANDROIDSECONDARY"
)
'''client = Client(
    certificate = "08dfef34d4d6fc8e7d138d683c229a8e76ffe4b40c6f459f43224053fbf09344",
    appType = "CHROMEOS"
)'''
'''client = Client(
    appType = "WEAROS"
)'''
'''client = Client(
    certificate = "4a808aed1454eeef2c7b3749b621028dffcda33b77ad90a92fe87f5754c193ef",
    appType = "IOSIPAD", workers = 5
)'''

'''client = Client(
    appType = "CHROMEOS"
)'''


@client.on_message(filters = filters.command("speed"), type = 25)
async def get_speed(_: Client, m: Message):
    s = time.time()
    await _.sendMessage(m.to, "Hi");await _.sendMessage(m.to, f"{round((time.time()-s)*1000)} ms.")

@client.on_message(type = 25, filters = filters.command("hi"))
async def get_hi(_: Client, m: Message):
    await _.sendMessage(m.to, "Hi tooo.")

@client.on_message(type = 25, filters = filters.regex(r"broadcast"))
async def broadcast(_: Client, m: Message):
    if not m.matches:
        return
    text = m.text[11:] if m.matches[0].start() == 1 else m.text[12:] if m.matches[0].start() == 2 else ""
    if text:
        async def main():
            result = await _.sendMessage(m.to, "Hello")
            res    = await _.sendMessage(m.to, "Hello too.")
        coros = [main() for i in range(10)]
        await asyncio.gather(*coros)

client.poll.run()
