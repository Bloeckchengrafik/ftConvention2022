import time
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
from detect.imtools import ImageTool

def errpaizeh():
    import rpyc

    conn = rpyc.connect("192.168.188.24", 18861)
    print(conn.root.sort(35077))


def cameraimage():
    import ftrobopy
    txt, frame = (None, None)
    while True:
        try:
            txt = ftrobopy.ftrobopy("192.168.188.25")
            if txt.getCameraFrame() == None:
                txt.startCameraOnline()
                time.sleep(2.5)

            frame = txt.getCameraFrame()
            frame = bytearray(frame)
            break
        except: pass
    frame_jpgdaten = BytesIO(frame)
    geladenes_bild = Image.open(frame_jpgdaten)
    bild = np.asarray(geladenes_bild)

    cv2.imshow("frame", bild)

    time.sleep(5)

    frame = txt.getCameraFrame()
    frame = bytearray(frame)
    frame_jpgdaten = BytesIO(frame)
    geladenes_bild = Image.open(frame_jpgdaten)
    bild = np.asarray(geladenes_bild)

    cv2.imshow("dimmed", bild)

    cv2.waitKey(0)
    txt.stopCameraOnline()


def croptest():
    im = cv2.imread("out/lit.png")
    imtool = ImageTool()
    rectangle = [45, 0, 230, 210]

    image = imtool.crop(im, *rectangle)

    mask = np.zeros(image.shape[:2], np.uint8)
  
    backgroundModel = np.zeros((1, 65), np.float64)
    foregroundModel = np.zeros((1, 65), np.float64)

    rectangle = [10, 10, 190, 210]

    cv2.grabCut(image, mask, rectangle, 
            backgroundModel, foregroundModel,
            3, cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8')
    image = image * mask2[:, :, np.newaxis]

    cv2.imshow("out/cropped.png", image)
    cv2.waitKey(0)


def colorcorrect():
    source = cv2.imread("out/unlit.png")
    cv2.imshow("source", source.copy())

    realcolor_yellow_bar = "d7ae00"
    realcolor_red_pin = "b8373b"



    cv2.waitKey(0)

colorcorrect()