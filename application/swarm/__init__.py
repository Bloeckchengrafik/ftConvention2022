from logging import info, debug, warn
import logging
import serial
import asyncio



class FtSwarm:
    objects = {}

    def __init__(self, port, dbg):
        self.ser = serial.Serial(port, 115200, timeout=5)
        self.oninput = asyncio.Event()
        self.line = ""
        self.debug = dbg
        info("Trying to reboot")

        self.ser.write("res\r\n".encode())

        warn("Waiting for a reset...")

        while self.ser.in_waiting <= 0:
            pass

        for i in range(13):
            message = self.ser.read_until(serial.LF)
            if i == 0:
                debug(f"Message from the ftSwarm:")
            try:
                debug("- " + message.decode("UTF-8").removesuffix("\r\n"))
            except: pass
        self.ser.read_all()
        info("Connected to ftSwarm")

    async def system(self, promt):
        self.ser.write(f"{promt}\r\n".encode())
        await self.oninput.wait()
        self.oninput.clear()
        return self.line

    async def get_obj(self, typeclass, name):
        if name in self.objects.keys():
            return self.objects[name]
        else:
            obj = typeclass(self, name)
            await obj.postinit()
            self.objects[name] = obj
            return obj

    async def get_switch(self, name):
        return await self.get_obj(FtSwarmSwitch, name)

    async def get_button(self, name):
        return await self.get_obj(FtSwarmButton, name)

    async def get_lightbarrier(self, name):
        return await self.get_obj(FtSwarmLightBarrier, name)

    async def get_reedswitch(self, name):
        return await self.get_obj(FtSwarmReedSwitch, name)
    
    async def get_motor(self, name):
        return await self.get_obj(FtSwarmMotor, name)
    
    async def get_lamp(self, name):
        return await self.get_obj(FtSwarmLamp, name)

    async def inputloop(self):
        while True:
            await asyncio.sleep(0.025)
            if self.ser.in_waiting > 0:
                line = self.ser.read_until().decode("utf-8")
                if not line.endswith("\n"):
                    warn(f"Expected Newline ({line})")
                line = line.removesuffix('\r\n')

                if line.startswith("#"):
                    print("\r", end="")

                    line = line.removeprefix("#").split(" ", 1)

                    logging.log(
                        logging._nameToLevel[line[0].upper()], f"- {line[1]}")
                    continue

                elif line.startswith("!"):
                    split = line[1:].split(" ", 1)
                    await self.objects[split[0]].handle_input(split[1])
                    if self.debug:
                        print("\r", end="")
                        debug(f"-!- {line}")

                    continue

                if self.debug:
                    print("\r", end="")
                    debug(f"- {line}")

                self.line = line
                self.oninput.set()

class FtSwarmSwitch:
    def __init__(self, swarm: FtSwarm, name) -> None:
        self.swarm = swarm
        self.name = name
        self.state = False
        self.events = []

    async def handle_input(self, inp):
        self.state = False if inp == "0" else True
        for event in self.events:
            event.set()

    async def postinit(self):
        await self.swarm.system("sub digital " + self.name)


class FtSwarmButton(FtSwarmSwitch):
    pass


class FtSwarmLightBarrier(FtSwarmSwitch):
    def closed(self):
        """
        Return if the light barrier is closed
        """

        return not self.state


class FtSwarmReedSwitch(FtSwarmSwitch):
    pass


class FtSwarmMotor:
    def __init__(self, swarm: FtSwarm, name) -> None:
        self.swarm = swarm
        self.name = name
        self.__speed = 0

    async def handle_input(self, inp):
        pass

    async def postinit(self):
        pass

    async def get_speed(self):
        return self.__speed

    async def set_speed(self, speed):
        await self.swarm.system(f"mot {self.name} {speed}")
        self.__speed = speed
    
class FtSwarmLamp(FtSwarmMotor):
    async def on(self, val):
        await self.set_speed(val)
    
    async def off(self):
        await self.set_speed(0)
