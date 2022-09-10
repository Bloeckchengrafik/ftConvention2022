from asyncio import Queue, sleep
from logging import info, debug, warn
from swarm import FtSwarm, Switch
from repl import detect_repl_event, latest_commands

swarm: FtSwarm = None

async def main(globalstate, pipe: Queue):
    global swarm

    swarm = globalstate["swarm"]

    while True:
        await sleep(0.25)
        command_result = await command_loop()

        if not command_result: continue

        warn("Detection is now working... Other commands may not work correctly. Please wait")
        switch: Switch = await swarm.get_switch("testbutton")

        for i in range(10):
            await sleep(0.5)
            info("State: %s", str(switch.state))


        await swarm.system("nod")
        info("Done! Part Number: ")


async def command_loop():
    if not detect_repl_event.is_set(): return None

    cmd = latest_commands["detect"]
    detect_repl_event.clear()

    return True if cmd == "" else bool(cmd)

    