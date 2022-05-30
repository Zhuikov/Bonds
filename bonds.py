#!/usr/bin/python3
import asyncio

from bondsRepoters import ConsoleReporter
from bondsManager import BondManager, BondRepositoryJson

async def main():
    repository = BondRepositoryJson("example.json")

    manager = BondManager(repository)
    repository.commit()
    await asyncio.wait((manager.initializeBondsParams(),), timeout=3)
    
    consoleReporter = ConsoleReporter()
    consoleReporter.report(manager.getBonds())

ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(main())
ioloop.close()
