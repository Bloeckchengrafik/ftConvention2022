import asyncio
from logging import info, critical
from threading import Thread
from detect.imtools import ImageTool
from ftrobopy import ftrobopy
from PIL import Image
import cv2
import time
from io import BytesIO
import numpy as np
import asyncio
import swarm

class EventTS(asyncio.Event):
    def set(self):
        super().set()

class ImageGatherThread(Thread):
    def values(self, event: EventTS, swarm: swarm.FtSwarm, stopmepls):
        self.event = event
        self.lit = None
        self.unlit = None
        self.swarm = swarm
        self.stopmepls = stopmepls
        return self

    async def ledon(self):
        await self.swarm.system("led on")


    async def ledoff(self):
        await self.swarm.system("led off")

    def run(self):
        txt = None
        time.sleep(0.1)
        while True:
            try:
                info("Trying to get Frame 1")
                txt = ftrobopy("192.168.188.25")
                if txt.getCameraFrame() == None:
                    txt.startCameraOnline()
                    time.sleep(3)
                frame = txt.getCameraFrame()
                frame = bytearray(frame)

                with open("out/capture0.jpg", "wb") as ifile:
                    ifile.write(frame)
                time.sleep(0.1)
                self.lit = cv2.imread("out/capture0.jpg")
                #self.lit = self.lit[:,:,::-1]
                break
            except Exception as e: 
                critical(e)
                if txt is not None:
                    try:
                        txt.stopCameraOnline()
                    except: pass
                    txt.stopOnline()
        info("Working on Im2")
        self.stopmepls.set()
        time.sleep(4)

        while True:
            try:
                frame = txt.getCameraFrame()
                frame = bytearray(frame)

                
                with open("out/capture1.jpg", "wb") as ifile:
                    ifile.write(frame)

                time.sleep(0.1)
                self.unlit = cv2.imread("out/capture1.jpg")
                #self.unlit = self.unlit[:,:,::-1]
                break
            except: pass
        
        txt.stopCameraOnline()
        txt.stopOnline()

        self.event.set()

class Detect(ImageTool):
    def __init__(self, swarm: swarm.FtSwarm):
        self.swarm = swarm

    async def images(self):
        info("Gathering image data...")
        led: swarm.FtSwarmMotor = await self.swarm.get_motor("sideled")

        event = EventTS()
        stopmepls = EventTS()
        th = ImageGatherThread().values(event, self.swarm, stopmepls)
        await th.ledon()
        await asyncio.sleep(0.5)
        await th.ledon()
        await asyncio.sleep(0.5)
        await th.ledon()
        await asyncio.sleep(0.5)
        await th.ledon()
        th.start()
        await stopmepls.wait()
        await led.set_speed(255)
        await th.ledoff()
        await th.ledoff()
        await th.ledoff()

        await event.wait()
        await led.set_speed(0)

        cv2.imwrite("out/lit.png", th.lit)
        cv2.imwrite("out/unlit.png", th.unlit)

        return (th.lit, th.unlit)

    async def cropimg(self, image, num):
        rectangle = [65, 10, 200, 190]

        cv2.imwrite(f"out/cropped{num}.png", self.crop(image, *rectangle))

        return self.crop(image, *rectangle)

    async def grabcut(self, image):
        image = await self.cropimg(image, 0)

        mask = np.zeros(image.shape[:2], np.uint8)
  
        backgroundModel = np.zeros((1, 65), np.float64)
        foregroundModel = np.zeros((1, 65), np.float64)

        rectangle = [5, 10, 190, 205]

        cv2.grabCut(image, mask, rectangle, 
            backgroundModel, foregroundModel,
            3, cv2.GC_INIT_WITH_RECT)

        mask2 = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8')
        image = image * mask2[:, :, np.newaxis]

        unique, counts = np.unique(mask2, return_counts=True)

        return image, mask2, dict(zip(unique, counts))[1]