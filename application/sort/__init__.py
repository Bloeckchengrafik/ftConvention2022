from asyncio import Queue
from logging import info, debug


async def main(globalstate, pipe: Queue):
    info("Synced 'sort'")
