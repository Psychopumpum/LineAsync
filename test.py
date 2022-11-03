#!usr/bin/python
# -*- coding: utf-8 -*-
import asyncio, time
from LineAsync import *

'''client = Client(
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5OTI5MTk5MC02MjI4LTQ1MWQtOGU4OS1kYmUwMDMyZDg1ZGMiLCJhdWQiOiJMSU5FIiwiaWF0IjoxNjY3MDY0NDUxLCJleHAiOjE2Njc2NjkyNTEsInNjcCI6IkxJTkVfQ09SRSIsInJ0aWQiOiI3ZWVhZDlmZi03ODY1LTQwMDktYTdjZi03N2ZjMTIzMjg4MDgiLCJyZXhwIjoxNjk4NjAwNDUxLCJ2ZXIiOiIzLjEiLCJhaWQiOiJ1MjQwYWY4MzVlNGMwMTk5MWNlN2ViNjk0ZWE2NTJjOGYiLCJsc2lkIjoiZmMzNWEzOTQtMTUwYi00ZTZiLWEwYTMtMGZmNjlmNTJhNzgyIiwiZGlkIjoiTk9ORSIsImN0eXBlIjoiQU5EUk9JRFNFQ09OREFSWSIsImNtb2RlIjoiU0VDT05EQVJZIiwiY2lkIjoiMDkwMDAwMDAwMCJ9.3yT6I5aK2cA9y3YE9dMQ3tJXHoYIBcEwyeDyE_U4_Bc",
    certificate = "32148f1f83cceff20f9629c0d000a16dc582cc42b01f6869facc01b78a17d93b",
    appType = "ANDROIDSECONDARY"
)'''
client = Client(
    "Fl8zOlOCUDSNJN9T35Uf.jaR4nEtagzhoFRAu6MuSJW.xlv8VQsE4P7ZG2Enn8a/t1j/mCMWhJtiNHkNKnpI9Ps=",
    certificate = "4a808aed1454eeef2c7b3749b621028dffcda33b77ad90a92fe87f5754c193ef",
    appType = "IOSIPAD", workers = 5
)


@client.hooks(type = 25, filters = filters.command("speed"))
async def get_speed(_: Client, m: Message):
    s = time.monotonic()
    await _.sendMessage(m.to, "Hi")
    await _.sendMessage(m.to, f"{round((time.monotonic()-s)*1000, 2)} ms.")

@client.hooks(type = 25, filters = filters.command("hi"))
async def get_hi(_: Client, m: Message):
    await _.sendMessage(m.to, "Hi tooo.")

client.poll.run()