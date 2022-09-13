from concurrent.futures import thread
import math
from detect.server import outqueue, inqueue
import cv2
import imutils
import numpy as np


class ImageTool:
    def get_img(self) -> cv2.Mat:
        inqueue.put(1)
        return outqueue.get()

    def crop(self, mat, x, y, h, w):
        return mat[y:y+h, x:x+w]

    def crop_and_scale_for_top_view(self, mat: cv2.Mat):
        mat = np.rot90(mat, 2)
        mat = self.crop(mat, 50, 0, 100, 100)
        return cv2.resize(mat, (50, 50)) 

    def desat(self, mat: cv2.Mat):
        hsvImageCopy = cv2.cvtColor(mat, cv2.COLOR_BGR2HSV)
        hsvImageCopy = np.float32(hsvImageCopy)
        saturationScale = 0.01
        H, S, V = cv2.split(hsvImageCopy)
        S = np.clip(S * saturationScale, 0, 255)
        hsvImageCopy = cv2.merge([H, S, V])
        hsvImageCopy = np.uint8(hsvImageCopy)
        hsvImageCopy = cv2.cvtColor(hsvImageCopy, cv2.COLOR_HSV2BGR)

        return hsvImageCopy

    def invert(self, mat: cv2.Mat):
        return (255-mat)

    
    def apply_soft_light(self, bottom, top):
        """ Apply soft light blending
        """

        result = np.zeros(bottom.shape, dtype=bottom.dtype)

        for y in range(bottom.shape[0]):
            for x in range(bottom.shape[1]):
                for col in range(bottom.shape[2]):
                    a = float(bottom[x][y][col])
                    b = float(top[x][y][col])

                    a = a/255
                    b = b/255

                    c = 0.0

                    if b < 0.5:
                        c = (2*a*b) + (a*a*(1-2*b))
                    else:
                        c = (2*a*(1-b)) + math.sqrt(a)*(2*b-1)
                    
                    c *= 255

                    result[y,x,col] = np.clip(int(c), 0, 255)

        return result
    
    def remove_shadows(self, img):
        rgb_planes = cv2.split(img)

        result_planes = []
        result_norm_planes = []
        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 21)
            diff_img = 255 - cv2.absdiff(plane, bg_img)
            norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            result_planes.append(diff_img)
            result_norm_planes.append(norm_img)

        result = cv2.merge(result_planes)
        result_norm = cv2.merge(result_norm_planes)

        return (result, result_norm)
    
    def sharpen(self, frame):
        image = cv2.GaussianBlur(frame, (0, 0), 3)
        return cv2.addWeighted(frame, 1.5, image, -0.5, 0)
    
    def get_edge(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        cv2.imwrite("out/gray.png", gray)
        thresh = cv2.Canny(gray, 100, 200)
        return thresh

    def get_elem(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray, (3, 3), 0)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        return thresh