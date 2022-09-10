from distutils.debug import DEBUG
from logging import info, debug, warn
import logging
import serial, asyncio

class FtSwarm:
    objects = {}

    def __init__(self, port, dbg):	
        self.ser = serial.Serial(port, 115200, timeout=5)
        self.oninput = asyncio.Event()
        self.line = ""
        self.debug = dbg
        warn("Waiting for a reset...")
    
        while self.ser.in_waiting <= 0: pass

        for i in range(13):
            message = self.ser.read_until(serial.LF)
            if i == 0: debug(f"Message from the ftSwarm:") 
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
        
    async def get_switch(self, name):
        return await self.get_obj(Switch, name)

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

                    logging.log(logging._nameToLevel[line[0].upper()], f"- {line[1]}")
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

class Switch:
    def __init__(self, swarm: FtSwarm, name) -> None:
        self.swarm = swarm
        self.name = name
        self.state = False

    async def handle_input(self, inp):
        self.state = False if inp == "0" else True

    async def postinit(self):
        debug("Calling Switch postinit for '%s'", self.name)
        await self.swarm.system("sub digital " + self.name)
