#!/usr/bin/python3
import asyncio

from bonds import Bond

bonds = [Bond("RU000A0JX0B9"), Bond("SU26220RMFS2")]

async def main():
    done, pending = await asyncio.wait([
        b.initializeBondParams() for b in bonds], timeout=1)
    print("done", done)
    for f in pending:
        print(f)

    for b in bonds:
        print(b)

ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(main())
# ioloop.close()
