from asyncio import Queue, sleep
from logging import info, debug, warn
from shutil import move
from swarm import FtSwarm
from .detection import Detect
from .movement import Movement
from .server import run as run_server
import threading
from repl import detect_repl_event, latest_commands
import cv2 as cv

swarm: FtSwarm = None

async def main(globalstate, pipe: Queue):
    global swarm

    swarm = globalstate["swarm"]

    movement = Movement(swarm)
    await movement.postinit()

    threading.Thread(target=run_server).start()
    
    while True:
        await sleep(0.25)
        command_result = await command_loop()

        if not command_result: continue

        warn("Detection is now working... Other commands may not work correctly. Please wait")
        detect = Detect(movement)
        await detect.optimize_turntable()

        info("Done! Part Number: ")


async def command_loop():
    if not detect_repl_event.is_set(): return None

    cmd = latest_commands["detect"]
    detect_repl_event.clear()

    return True if cmd == "" else bool(cmd)

    