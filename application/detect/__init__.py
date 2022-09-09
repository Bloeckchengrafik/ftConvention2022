from asyncio import Queue
from logging import info, debug
from helpers import ainput
from swarm import FtSwarm

swarm: FtSwarm = None

async def main(globalstate, pipe: Queue):
    global swarm
    info("Synced 'detect'")

    swarm = globalstate["swarm"]
    
    while True:
        cmd = await ainput("")
        debug("Sending...")
        swarm.ser.write(f"{cmd}\r\n".encode("utf-8"))
        await swarm.oninput.wait()
        debug(f"Got Event: {swarm.line}")
        

    
