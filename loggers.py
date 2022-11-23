# -*- coding: utf-8 -*-
from LineAsync import *
import asyncio, sys

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

async def main(op):
    try:
        parser.log("Initializing...", color = "BLUE")
    except Exception:
        traceback.print_exc()
    except KeyboardInterrupt:
      sys.exit("Keyboard interrupted.")

async def fetching():
    try:
        while not client.poll.fetch_event.is_set():
            ops = await client.poll.fetchOps(100)
            for op in ops:
                if op.revision == -1 and op.param2 != None:
                    client.poll.globalRev = int(op.param2.split("\x1e")[0])
                if op.revision == -1 and op.param1 != None:
                    client.poll.individualRev = int(op.param1.split("\x1e")[0])
                await client.poll.setRevision(op.revision)
                await asyncio.ensure_future(main(op))
    except Exception:
        traceback.print_exc()
    except KeyboardInterrupt:
        sys.exit("Keyboard interrupted.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetching())