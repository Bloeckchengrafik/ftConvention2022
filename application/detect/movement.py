from math import floor
from swarm import *
from asyncio import sleep

class Movement:
    turntable: FtSwarmMotor
    def __init__(self, swarm: FtSwarm) -> None:
        self.swarm = swarm

    async def postinit(self):
        self.turntable = await self.swarm.get_motor("Drehscheibe")

    async def turnTurntable(self, goodness):
        while True:
            how_good = await goodness()

            quality_str = "|         ---         |"

            index = floor(how_good*10)+11   
            quality_str = quality_str[:index] + "#" + quality_str[index + 1:]

            speed = max(int(min(how_good*50, 20)), 14)

            info("Current Quality: %s (%f / Speed: %d)", quality_str, how_good, speed)

            if how_good == 0:
                await self.turntable.set_speed(0)
                return

            await self.turntable.set_speed(speed)

            await sleep(0.2)

            await self.turntable.set_speed(0)
            
            await sleep(0.3)


