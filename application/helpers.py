import asyncio, sys

async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s+' '))
    sys.stdout.flush()
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)
