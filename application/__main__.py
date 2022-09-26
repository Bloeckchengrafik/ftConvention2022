from asyncio import Queue, gather as gather_tasks, run
from optparse import OptionParser
import time
from platformio.device.finder import SerialPortFinder 
import sys, os
from logging import error, info, debug
import logging
import coloredlogs
import pickle

from detect import main as detect
from gather import main as gather
from sort import main as sort
from repl import main as repl
from swarm import FtSwarm
from values import VERSION
from repl.splash import print_splash
from helpers import maximize_console

opt = OptionParser(version=VERSION)

opt.add_option("-c", "--compile", help="Compile the program", action="store_true", default=False, dest="do_compile")
opt.add_option("-u", "--upload", help="Upload the program", action="store_true", default=False, dest="do_upload")
opt.add_option("-d", "--debug", help="Start Application with all logs enabled", action="store_true", default=False, dest="debuglogger")
opt.add_option("-a", "--app", help="Start the app", action="store_true", default=False, dest="do_app")

sys.argv[0] = "convention"

(args, _) = opt.parse_args()

maximize_console()
time.sleep(0.5)

coloredlogs.install(level=logging.DEBUG if args.debuglogger else logging.INFO, fmt="\r[%(asctime)s / %(name)-10s] %(levelname)-7s %(message)s")

os.chdir("../sketch")
debug("Went to Sketch Directory")

if args.do_compile:
    os.system("py -m platformio run")

if args.do_upload:
    os.system("py -m platformio run -t upload")


if not args.do_app:
    logging.info("Done!")
    exit(0)


os.chdir("../application")
debug("Returned")


portfiner = SerialPortFinder()

globalstate = {
    "current_part": 0,
    "swarm": None,
    "partdata": [
        # [area, color]: pid
    ]
}

detect_queue = Queue()
gather_queue = Queue()
sort_queue = Queue()

async def try_run(coro):
    try:
        await coro
    except Exception as e:
        error("Application failed", exc_info=e)

async def main():
    print_splash()

    withswarm = []

    globalstate["swarm"] = FtSwarm(portfiner.find(),  args.debuglogger)

    withswarm += [
            globalstate["swarm"].inputloop()
    ]
    
    withswarm += [
        detect(globalstate, detect_queue),
        gather(globalstate, gather_queue)
    ]

    withtxt = [
        sort(globalstate, sort_queue)
    ]

    all = withswarm + withtxt

    await gather_tasks(
        *[try_run(a) for a in all],
        repl(globalstate))


if __name__ == "__main__":
    try:
        run(main())
    except Exception as e:
        logging.error("Application failed:", exc_info=e)
        input()