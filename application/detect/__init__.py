from asyncio import Queue, sleep
from logging import critical, info, debug, warn
from swarm import FtSwarm
from .detection import Detect
from repl import detect_repl_event, latest_commands
import cv2 as cv
from events import gather_done_event, detect_done_event

swarm: FtSwarm = None

async def main(globalstate, pipe: Queue):
    global swarm

    swarm = globalstate["swarm"]

    while True:
        await sleep(0.25)
        command_result = await command_loop()

        if command_result is None:
            continue

        warn("Detection is now working... Other commands may not work correctly. Please wait")
        detect = Detect(swarm)
        lit = None
        unlit = None

        if command_result:
            (lit, unlit) = await detect.images()
        else:
            lit = cv.imread("out/lit.png")
            unlit = cv.imread("out/unlit.png")
        
        grabbed,mask,area = await detect.grabcut(lit)

        unlit = await detect.cropimg(unlit, 1)

        avg = [0,0,0]
        avgamount = 0

        for x in range(unlit.shape[0]):
            for y in range(unlit.shape[1]):
                if mask[x][y] != 0:
                    color = unlit[x][y]
                    avg[0] += color[0]
                    avg[1] += color[1]
                    avg[2] += color[2]
                    avgamount += 1

        if avgamount == 0:
            critical("OH NO")
        
        avg[0] = int(avg[0] / avgamount)
        avg[1] = int(avg[1] / avgamount)
        avg[2] = int(avg[2] / avgamount)

        avg[0], avg[2] = avg[2], avg[0]

        cv.imwrite("out/grabbed.png", grabbed)

        info(f"Matching Area: {area}")
        info(f"Matching Color: {'#%02x%02x%02x' % tuple(avg)}")
        info("Done! Part Number: ")
        detect_done_event.set()


async def command_loop():
    if gather_done_event.is_set():
        gather_done_event.clear()
        return True

    if not detect_repl_event.is_set(): return None

    cmd = latest_commands["detect"]
    detect_repl_event.clear()

    print("-", cmd, "-")

    return True if cmd == "" else (True if cmd == "True" else False)

    