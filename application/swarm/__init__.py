from logging import info, debug, warn
import logging
import serial
import asyncio


class FtSwarm:
    pass


class FtSwarmSwitch:
    def __init__(self, swarm: FtSwarm, name) -> None:
        self.swarm = swarm
        self.name = name
        self.state = False

    async def handle_input(self, inp):
        self.state = False if inp == "0" else True

    async def postinit(self):
        await self.swarm.system("sub digital " + self.name)


class FtSwarmButton(FtSwarmSwitch):
    pass


class FtSwarmLightBarrier(FtSwarmSwitch):
    pass


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
    


class FtSwarm:
    objects = {}

    def __init__(self, port, dbg):
        self.ser = serial.Serial(port, 115200, timeout=5)
        self.oninput = asyncio.Event()
        self.line = ""
        self.debug = dbg
        warn("Waiting for a reset...")

        while self.ser.in_waiting <= 0:
            pass

        for i in range(13):
            message = self.ser.read_until(serial.LF)
            if i == 0:
                debug(f"Message from the ftSwarm:")
            debug("- " + message.decode("UTF-8").removesuffix("\r\n"))
        self.ser.read_all()
        info("Connected to ftSwarm")

    async def system(self, promt):
        self.ser.write(f"{promt}\r\n".encode())
        await self.oninput.wait()
        self.oninput.clear()
        return self.line

    async def get_obj(self, typeclass, name):
        try:
            return self.objects[name]
        except KeyError:
            obj = typeclass(self, name)
            await obj.postinit()
            self.objects[name] = obj
            return obj

    async def get_switch(self, name) -> FtSwarmSwitch:
        return await self.get_obj(FtSwarmSwitch, name)

    async def get_button(self, name) -> FtSwarmButton:
        return await self.get_obj(FtSwarmButton, name)

    async def get_lightbarrier(self, name) -> FtSwarmLightBarrier:
        return await self.get_obj(FtSwarmLightBarrier, name)

    async def get_reedswitch(self, name) -> FtSwarmReedSwitch:
        return await self.get_obj(FtSwarmReedSwitch, name)
    
    async def get_motor(self, name) -> FtSwarmMotor:
        return await self.get_obj(FtSwarmMotor, name)

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
                    continue

                elif self.debug:
                    print("\r", end="")
                    debug(f"- {line}")

                self.line = line
                self.oninput.set()
