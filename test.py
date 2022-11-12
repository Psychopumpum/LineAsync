#!usr/bin/python
# -*- coding: utf-8 -*-
import asyncio, time
from LineAsync import *

import concurrent.futures

client = Client(
    certificate = "32148f1f83cceff20f9629c0d000a16dc582cc42b01f6869facc01b78a17d93b",
    appType = "ANDROIDSECONDARY"
)
'''client = Client(
    certificate = "08dfef34d4d6fc8e7d138d683c229a8e76ffe4b40c6f459f43224053fbf09344",
    appType = "CHROMEOS"
)'''
'''client = Client(
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1ODA3NzIzNS0zMzNlLTQzYmUtYjNlOS0wMWY0YzY5MTc5NzIiLCJhdWQiOiJMSU5FIiwiaWF0IjoxNjY4MDUyMzkwLCJleHAiOjE2Njg2NTcxOTAsInNjcCI6IkxJTkVfQ09SRSIsInJ0aWQiOiI1N2QxODQ2My02YTkxLTQ0MGMtYWJjZi05NWMzOGIxODBiMWEiLCJyZXhwIjoxNjk5NTg4MzkwLCJ2ZXIiOiIzLjEiLCJhaWQiOiJ1MjQwYWY4MzVlNGMwMTk5MWNlN2ViNjk0ZWE2NTJjOGYiLCJsc2lkIjoiMmZhNzE0YTItYjk3Ni00NzQ4LWE1MWUtMTc3YzdjODc2ZDE5IiwiZGlkIjoiTk9ORSIsImN0eXBlIjoiV0VBUk9TIiwiY21vZGUiOiJTRUNPTkRBUlkiLCJjaWQiOiIwQTAwMDAwMDAwIn0.OkBJkwa6Tadp3kSbNDgekM10tS9tmybXAyX8VOXh4gU",
    appType = "WEAROS"
)'''
'''client = Client(
    "Fl8zOlOCUDSNJN9T35Uf.jaR4nEtagzhoFRAu6MuSJW.xlv8VQsE4P7ZG2Enn8a/t1j/mCMWhJtiNHkNKnpI9Ps=",
    certificate = "4a808aed1454eeef2c7b3749b621028dffcda33b77ad90a92fe87f5754c193ef",
    appType = "IOSIPAD", workers = 5
)'''

'''client = Client(
    appType = "CHROMEOS"
)'''


@client.on_message(filters = filters.command("speed"), type = 25)
async def get_speed(_: Client, m: Message):
    s = time.time()
    await _.sendMessage(m.to, "Hi")
    await _.sendMessage(m.to, f"{round((time.time()-s)*1000)} ms.")

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
