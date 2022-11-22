# -*- coding: utf-8 -*-
from LineAsync import *
import asyncio

parser = ColoredArgumentParser()
for arg in Args:
    parser.add_argument(
        arg['short_name'],
        arg['long_name'],
        help=arg['help'],
        type=arg['type']
    )
args = parser.parse_args()

if not args:
    parser.error("Need an argument to run the bots.")
elif args:
    if not args.mid:
        parser.error("Argument -u --mid are needed.")
    elif not args.apptype:
        args.apptype = "IOSIPAD"
    elif not args.name:
        parser.error("Argument -n --name are needed.")
    elif not args.token:
        args.token = ""
    elif not args.certificate:
        args.certificate = ""

client = Client(args.token, certificate = args.certificate, mid = args.mid, name = args.name, appType = args.apptype)

async def main():
    parser.log("Initializing...", color = "BLUE")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())