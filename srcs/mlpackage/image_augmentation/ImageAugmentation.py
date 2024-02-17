import numpy as np
import cv2 as cv
from plantcv import plantcv as pcv
import random


class ImageAugmentation:

    def read_image(filename):
        img, _, _ = pcv.readimage(filename)
        if img is None:
            raise Exception("The file is not an image")
        return img

    def contrast(img, alpha=-100, beta=2):
        contrast = img.copy()
        for y in range(contrast.shape[0]):
            for x in range(contrast.shape[1]):
                for c in range(contrast.shape[2]):
                    contrast[y][x][c] = np.clip(
                        alpha + contrast[y][x][c] * beta,
                        0,
                        255
                    )
        return contrast

    def brightness(img, gam=0.5):
        def gamma(pixel, gam):
            return [
                (pixel[0] / 255) ** gam * 255,
                (pixel[1] / 255) ** gam * 255,
                (pixel[2] / 255) ** gam * 255
            ]
        bright = img.copy()
        for y in range(bright.shape[0]):
            for x in range(bright.shape[1]):
                bright[y][x] = gamma(bright[y][x], gam)
        return bright

    def flip(img, direction="vertical"):
        return pcv.flip(img, direction)

    def rotate(img, angle=np.random.randint(0, 360)):
        return pcv.transform.rotate(img, angle, crop=True)

    def blur(img, kernel_size=(5, 5)):
        return pcv.gaussian_blur(img, kernel_size, 1)

    def newPoint(x, y):
        return [
            random.randint(int(x * 0.1), int(x * 0.9)),
            random.randint(int(x * 0.1), int(y * 0.9))
        ]

    def nextP(p, x, y):
        xf = int(x * 0.2)
        yf = int(y * 0.2)
        return [
            (p[0] + random.randint(0, xf) % x),
            (p[1] + random.randint(0, yf)) % y
        ]

    def distortion(img):
        img_height, img_width, _ = np.shape(img)
        A = [0, 0]
        B = [0, random.randint(0, int(img_height * 0.1))]
        C = [img_width, random.randint(0, int(img_height * 0.1))]
        pt1 = np.float32(
            [A, B, C]
        )
        pt2 = np.float32(
            [A, B, ImageAugmentation.nextP(C, img_width, img_height)]
        )
        M = cv.getAffineTransform(pt1, pt2)
        dst = cv.warpAffine(img, M, (img_width, img_height))
        return dst

    def zoom(img):
        img_height, img_width, _ = np.shape(img)
        scale_w = np.random.randint(0, int(img_width * 0.25))
        scale_h = scale_w * img_height / img_width
        pt1 = np.float32([
            [0, 0],
            [0, img_height],
            [img_width, 0],
            [img_width, img_height]
        ])
        pt2 = np.float32([
            [scale_w, scale_h],
            [scale_w, img_height - scale_h],
            [img_width - scale_w, scale_h],
            [img_width - scale_w, img_height - scale_h]
        ])
        M = cv.getPerspectiveTransform(pt2, pt1)
        zoom = cv.warpPerspective(img, M, (img_width, img_height))
        return zoom
