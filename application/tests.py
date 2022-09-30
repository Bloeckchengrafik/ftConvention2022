import os
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


def ReGrab():
    source = cv2.imread("out/lit.png")

    lab= cv2.cvtColor(source, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l_channel)
    limg = cv2.merge((cl,a,b))
    source = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    imtool = ImageTool()
    rectangle = [65, 11, 190, 190]

    source2 = np.ones_like(source)

    source = imtool.crop(source, *rectangle)

    source = cv2.GaussianBlur(source, (3, 3), 1)

    old_image_height, old_image_width, channels = source.shape
    new_image_height, new_image_width, _ = source2.shape
    color = (255,248,248)
    res = np.full((new_image_height,new_image_width, channels), color, dtype=np.uint8)
    x_center = (new_image_width - old_image_width) // 2
    y_center = (new_image_height - old_image_height) // 2

    res[y_center:y_center+old_image_height, 
       x_center:x_center+old_image_width] = source

    source = res
    cv2.imshow("crp", source.copy())

    mask = np.zeros(source.shape[:2], np.uint8)
  
    backgroundModel = np.zeros((1, 65), np.float64)
    foregroundModel = np.zeros((1, 65), np.float64)

    cv2.grabCut(source, mask, rectangle, 
            backgroundModel, foregroundModel,
            3, cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8')
    source = source * mask2[:, :, np.newaxis]

    cv2.imshow("regrab", source.copy())


    cv2.waitKey(0)
    cv2.destroyAllWindows()

ReGrab()
os.system("py tests.py")
