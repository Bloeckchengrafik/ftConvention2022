from distutils.debug import DEBUG
from logging import info, debug, warn, error
import logging
import serial, asyncio

class FtSwarm:
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

    async def inputloop(self):
        while True:
            await asyncio.sleep(0.025)
            if self.ser.in_waiting > 0:
                line = self.ser.read_until().decode("utf-8")
                if not line.endswith("\n"):
                    error("Application Failed: ", Exception("Broken Pipe: ", line))
                line = line.removesuffix('\r\n')
                
                if line.startswith("#"):
                    print("\r", end="")

                    line = line.removeprefix("#").split(" ", 1)

                    logging.log(logging._nameToLevel[line[0].upper()], f"- {line[1]}")
                    continue
                

                elif self.debug:
                    print("\r", end="")
                    debug(f"- {line}")
                
                self.line = line
                pass
                self.oninput.set()