from asyncio import Queue, sleep
import asyncio
from logging import critical, info, debug, warn
from helpers import adialogbox, prCyan, prRed
from swarm import FtSwarm, FtSwarmMotor, FtSwarmSwitch
from .detection import Detect
from repl import detect_repl_event, latest_commands
import cv2 as cv
from events import gather_done_event, detect_done_event
from values import CALIB_IN_PROGRESS
from db import db
import numpy as np

swarm: FtSwarm = None

async def main(globalstate, pipe: Queue):
    global swarm

    swarm = globalstate["swarm"]

    endstoplower: FtSwarmSwitch = await swarm.get_button("endstoplower")              
    endstoptop: FtSwarmSwitch = await swarm.get_button("endstoptop")                    
    motoben: FtSwarmMotor  = await swarm.get_motor("motoben")                        

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

        grabbed,mask,area = await detect.recut(lit)

        unlit = cv.copyMakeBorder(unlit, 13, 0, 0, 0, cv.BORDER_CONSTANT, None, value = 0)

        avg = [0,0,0]
        avgamount = 0

        colormask = np.zeros_like(unlit)

        for x in range(lit.shape[0]):
            for y in range(lit.shape[1]):
                if mask[x][y] != 0:
                    color = unlit[x][y]
                    avg[0] += color[0]
                    avg[1] += color[1]
                    avg[2] += color[2]
                    avgamount += 1
                    colormask[x][y] = color

        cv.imwrite("out/cmask.png", colormask)

        if avgamount == 0:
            critical("OH NO")
        
        avg[0] = int(avg[0] / avgamount)
        avg[1] = int(avg[1] / avgamount)
        avg[2] = int(avg[2] / avgamount)

        avg[0], avg[2] = avg[2], avg[0]

        cv.imwrite("out/grabbed.png", grabbed)

        info(f"Matching Area: {area}")
        info(f"Matching Color: {'#%02x%02x%02x' % tuple(avg)}")

        pid = -1

        if CALIB_IN_PROGRESS:
            info("Calibrating...")
            info("Color Category:")
            colorcategories = db.proxy.keys()

            for num, cat in enumerate(colorcategories):
                info(f" - {cat} ({num})")
            
            catname = list(colorcategories)[int(await adialogbox("calibrate$ "))]
            info(f"Chose '{catname}'")

            cat = db.proxy[catname]

            info("Choose part:")
            for num, cattext in enumerate(cat["parts"].keys()):
                info(f" - {cattext} ({num})")

            partname = list(cat["parts"].keys())[int(await adialogbox("part$ "))]

            info(f"Using PType: {catname}/{partname}")

            pid = cat["parts"][partname]["pid"]

            bounds = db.proxy[catname]["bounds"]

            if bounds["upper"][0] < avg[0]: bounds["upper"][0] = avg[0]
            if bounds["upper"][1] < avg[1]: bounds["upper"][1] = avg[1]
            if bounds["upper"][2] < avg[2]: bounds["upper"][2] = avg[2]

            if bounds["lower"][0] > avg[0]: bounds["lower"][0] = avg[0]
            if bounds["lower"][1] > avg[1]: bounds["lower"][1] = avg[1]
            if bounds["lower"][2] > avg[2]: bounds["lower"][2] = avg[2]
            print(bounds)
        
        else:
            colorcats = list(db.proxy.keys())

            currenthsv = cv.cvtColor(np.uint8([[avg]]), cv.COLOR_BGR2HSV)[0][0]
            currenthue = currenthsv[0]
            medianhues = [(int(cv.cvtColor(np.uint8([[y["upper"]]]), cv.COLOR_BGR2HSV)[0][0][0]) + int(cv.cvtColor(np.uint8([[y["lower"]]]), cv.COLOR_BGR2HSV)[0][0][0]))/2 for y in [db.proxy[x]["bounds"] for x in colorcats]]

            nearnessvals = [abs((y if y < 127 else y -127)) for y in [max(x, currenthue) - min(x, currenthue) for x in medianhues]]
            near = sorted(zip(colorcats, nearnessvals), key=lambda x:x[1])

            info(f"Nearest Color: {near[0]} @ HSV={currenthsv}, would nominate {near[0][0]}/[{' | '.join([x for x in db.proxy[near[0][0]]['parts']])}]")

            nominations = db.proxy[near[0][0]]['parts']
            color = near[0][0]

            if currenthsv[1] < 80:
                debug("Detected desat!")
                if currenthsv[2] > 140:
                    info("It is gray")
                    nominations = db.proxy["gray"]['parts']
                else:
                    nominations = db.proxy["black"]['parts']
                    color = "black"

            info(f"Determined the following: Part is Col/{color} with Nom/{nominations}")

            insideout = [(nominations[x]["vals"], nominations[x]["pid"], x ) for x in nominations.keys()]
            good_insideout = []
            for i in insideout.copy():
                good_insideout.extend([(abs(area - x), *(i[1:])) for x in i[0]])

            good_insideout = list(reversed(sorted(good_insideout, key=lambda x: x[0])))

            info("--- Part Detection Finals ---")
            
            method = prCyan

            for p in good_insideout:
                info(method(f"{(str(p[0])+'pp').rjust(5)}    col/{color.ljust(8)}    pid/{str(p[1]).ljust(6)}    name/{p[2]}"))
                if method == prCyan:
                    method = prRed
            info("-----------------------------")

            pid = good_insideout[0][1]

        await motoben.set_speed(255)
        await endstoptop.wait()
        await motoben.set_speed(50)
        await asyncio.sleep(2)
        await motoben.set_speed(0)
        await endstoplower.wait()
        await motoben.set_speed(200)
        await endstoplower.wait()
        await motoben.set_speed(0) 

        info(f"Done! Part Number: {pid}")
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

    