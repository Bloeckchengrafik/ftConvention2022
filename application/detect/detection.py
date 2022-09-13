from email.mime import image
from logging import info
from detect.imtools import ImageTool
from detect.movement import Movement
import cv2 as cv


class Detect(ImageTool):
    def __init__(self, movement: Movement) -> None:
        self.mv = movement

    async def turntable_check_optimized(self) -> float:    
        img = self.crop_and_scale_for_top_view(self.get_img())
        img = self.sharpen(img)
        cv.imwrite("out/sharpened.png", img)

        img, _ = self.remove_shadows(img)
        img, _ = self.remove_shadows(img)

        cv.imwrite("out/shadows.png", img)

        desat = self.desat(img)
        inverted_desat = self.invert(desat)
        softlight = self.apply_soft_light(img, inverted_desat)
        softlight = self.sharpen(softlight)
        thresh = self.get_elem(softlight)

        edge = img

        for x in range(50):
            for y in range(50):
                edge[x][y] = (0, 0, 0)
                if thresh[x][y] > 1:
                    edge[x][y] = (255, 255, 255)
        
        cv.imwrite("out/edge.png", edge)
        cv.imwrite("out/sl.png", softlight)
        return 0

    async def optimize_turntable(self) -> None:
        await self.mv.turnTurntable(self.turntable_check_optimized)
        