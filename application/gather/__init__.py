from logging import info
from asyncio import Queue, sleep, Event
from swarm import FtSwarm, FtSwarmMotor, FtSwarmSwitch
from repl import gather_repl_event
from events import sort_done_event, gather_done_event


async def main(globalstate, pipe: Queue):
    swarm: FtSwarm = globalstate["swarm"]
    belt_back: FtSwarmMotor = await swarm.get_motor("beltback")
    belt_front: FtSwarmMotor = await swarm.get_motor("beltfront")
    lightbarrier_belt: FtSwarmSwitch = await swarm.get_switch("lightbarrierbelt")

    lb_event = Event()

    lightbarrier_belt.events.append(lb_event)

    while True:
        await sleep(0.25)

        if not (gather_repl_event.is_set() or sort_done_event.is_set()):
            continue

        gather_repl_event.clear()
        sort_done_event.clear()

        await run(belt_back, belt_front, lb_event)
        
        await sleep(120)
        gather_repl_event.set()

async def run(belt_back: FtSwarmMotor, belt_front: FtSwarmMotor, lb_event: Event):
    info("Beginning the pipeline with gathering a part...")

    await belt_front.set_speed(70)
    await belt_back.set_speed(25)
    lb_event.clear() 
    await lb_event.wait()
    lb_event.clear() 
    await lb_event.wait()
    lb_event.clear() 
    await belt_back.set_speed(0)
    await belt_front.set_speed(50)
    await sleep(1)
        
    await belt_front.set_speed(0)

    info("Done! A part is now on the camera driver")
    gather_done_event.set()


    
