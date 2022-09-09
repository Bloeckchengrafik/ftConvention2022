from logging import info, debug
from asyncio import Queue

async def main(globalstate, pipe: Queue):
    info("Synced 'gather'")
