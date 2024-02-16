import argparse
from plantcv import plantcv as pcv
import random
import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


def parse_argument():
    parser = argparse.ArgumentParser(
        prog='Augmentation',
        description='This program balance the number of images' +
                    'for each variety and disease'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    return args.filename


def img_contrast(img, alpha=-100, beta=2):
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


def img_brightness(img, gam=0.5):

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


def img_flip(img, direction="vertical"):
    return pcv.flip(img, direction)


def img_rotate(img, angle=np.random.randint(0, 360)):
    return pcv.transform.rotate(img, angle, crop=True)


def img_blur(img, kernel_size=(5, 5)):
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


def img_distortion(img):
    img_height, img_width, _ = np.shape(img)
    A = [0, 0]
    B = [0, random.randint(0, int(img_height * 0.1))]
    C = [img_width, random.randint(0, int(img_height * 0.1))]
    pt1 = np.float32([A, B, C])
    pt2 = np.float32([A, B, nextP(C, img_width, img_height)])
    M = cv.getAffineTransform(pt1, pt2)
    dst = cv.warpAffine(img, M, (img_width, img_height))
    return dst


def img_zoom(img):
    img_height, img_width, _ = np.shape(img)
    scale_w = np.random.randint(0, int(img_width * 0.25))
    scale_h = scale_w * img_height / img_width

    pt1 = np.float32(
        [[0, 0],
         [0, img_height],
         [img_width, 0],
         [img_width, img_height]]
    )

    pt2 = np.float32(
        [[scale_w, scale_h],
         [scale_w, img_height - scale_h],
         [img_width - scale_w, scale_h],
         [img_width - scale_w, img_height - scale_h]]
    )
    M = cv.getPerspectiveTransform(pt2, pt1)
    zoom = cv.warpPerspective(img, M, (img_width, img_height))
    return zoom


def main():

    filename = parse_argument()

    if not os.path.exists(filename):
        raise Exception("The path does not exist")
    elif not os.path.isfile(filename):
        raise Exception("The path is not a file")

    img, path, name = pcv.readimage(filename)
    if img is None:
        raise Exception("The file is not an image")

    contrast = img_contrast(img)
    bright = img_brightness(img)
    flipped = img_flip(img)
    rotated = img_rotate(img)
    blurred = img_blur(img)
    zoomed = img_zoom(img)
    distortion = img_distortion(img)

    fig, axs = plt.subplots(2, 4)

    imgs = [
        img, contrast, bright, zoomed,
        flipped, rotated, blurred, distortion
    ]

    labels = [
        'Original', 'Contrast', 'Brightness', 'Zoomed',
        'Flipped', 'Rotated', 'Blurred', 'Distortion'
    ]

    for i, ax in enumerate(axs.flat):

        ax.imshow(imgs[i])
        ax.set_title(labels[i])

        ax.set(xticks=[], yticks=[])
        ax.label_outer()

    point_pos = filename.rfind(".")

    if point_pos == -1:
        extension = ""
    else:
        extension = filename[point_pos:]

    for i, image in enumerate(imgs):
        image_name = "./Image1002" + "_" + labels[i] + extension
        cv.imwrite(image_name, image)
    plt.show()


if __name__ == "__main__":

    try:
        main()
    except Exception as error:
        print(error)
        exit(1)
