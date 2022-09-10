from asyncio import Queue, gather as gather_tasks, run
from optparse import OptionParser
import time
from platformio.device.finder import SerialPortFinder 
import sys, os
from logging import info, debug
import logging
import coloredlogs

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
opt.add_option("-a", "--app", help="Start Application Service", action="store_true", default=False, dest="do_app")

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

info("Detecting Port..")

portfiner = SerialPortFinder()

globalstate = {
    "current_part": Queue(),
    "swarm": None
}

detect_queue = Queue()
gather_queue = Queue()
sort_queue = Queue()

async def main():
    print_splash()

    globalstate["swarm"] = FtSwarm(portfiner.find(),  args.debuglogger)
    await gather_tasks(
        detect(globalstate, detect_queue),
        gather(globalstate, gather_queue),
        sort(globalstate, sort_queue),
        repl(globalstate),
        globalstate["swarm"].inputloop(),
        return_exceptions=True
    )


if __name__ == "__main__":
    try:
        run(main())
    except Exception as e:
        logging.error("Application failed:", exc_info=e)
        input()