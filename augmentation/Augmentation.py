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




def img_contrast(img, alpha, beta):
    contrast = img.copy()
    for y in range(contrast.shape[0]):
        for x in range(contrast.shape[1]):
            for c in range(contrast.shape[2]):
                contrast[y][x][c] = np.clip(alpha + contrast[y][x][c] * beta, 0, 255)
    return contrast


def img_brightness(img, gam):

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


def img_flip(img, direction):
    return pcv.flip(img, direction)


def img_rotate(img, angle):
    return pcv.transform.rotate(img, angle, crop=False)


def img_blur(img, kernel_size):
    return pcv.gaussian_blur(img, kernel_size, 1)


def newPoint(x, y):
    return ([random.randint(int(x * 0.1), int(x * 0.9)), random.randint(int(x * 0.1), int(y * 0.9))])


def nextP(p, x, y):
    xf = int(x * 0.2)
    yf = int(y * 0.2)
    return ([(p[0] + random.randint(0, xf)%x), (p[1] + random.randint(0, yf))%y])


def img_distortion(img, img_width, img_height):
    img_height, img_width, _ = np.shape(img)
    A = [0, 0]
    B = [0, random.randint(0, int(img_height * 0.1))]
    C = [img_width, random.randint(0, int(img_height * 0.1))]
    pt1 = np.float32([A, B, C])
    pt2 = np.float32([A, B, nextP(C, img_width, img_height)])
    M = cv.getAffineTransform(pt1, pt2)
    dst = cv.warpAffine(img, M, (img_width, img_height))
    return dst


def img_zoom(img, img_width, img_height):
    scale_w = np.random.randint(0, int(img_width * 0.25))
    scale_h = scale_w * img_height / img_width
    pt1 = np.float32([[0, 0], [0, img_height], [img_width, 0], [img_width, img_height]])
    pt2 = np.float32([[scale_w, scale_h], [scale_w, img_height - scale_h], [img_width - scale_w, scale_h], [img_width - scale_w, img_height - scale_h]])
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

    contrast = img_contrast(img, -100, 2)
    bright = img_brightness(img, 0.5)
    flipped = img_flip(img, "vertical")
    rotated = img_rotate(img, random.randint(0, 360))
    blurred = img_blur(img, (5, 5))
    zoomed = img_zoom(img, img.shape[0], img.shape[1])
    distortion = img_distortion(img, img.shape[0], img.shape[1])

    # pcv.plot_image(img)
    # pcv.plot_image(contrast)
    # pcv.plot_image(bright)
    # pcv.plot_image(flipped)
    # pcv.plot_image(rotated)
    # pcv.plot_image(blurred)
    # pcv.plot_image(zoomed)
    # pcv.plot_image(distortion)

    fig, axs = plt.subplots(2, 4)
    axs[0, 0].imshow(img)
    axs[0, 1].imshow(contrast)
    axs[0, 2].imshow(bright)
    axs[0, 3].imshow(zoomed)
    axs[1, 0].imshow(flipped)
    axs[1, 1].imshow(rotated)
    axs[1, 2].imshow(blurred)
    axs[1, 3].imshow(distortion)


    axs[0, 0].set_title('Original')
    axs[0, 1].set_title('Contrast')
    axs[0, 2].set_title('Brightness')
    axs[0, 3].set_title('Zoomed')
    axs[1, 0].set_title('Flipped')
    axs[1, 1].set_title('Rotated')
    axs[1, 2].set_title('Blurred')
    axs[1, 3].set_title('Distortion')

    # Do not display the axis
    for ax in axs.flat:
        ax.set(xticks=[], yticks=[])

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    imgs = [img, contrast, bright, zoomed, flipped, rotated, blurred, distortion]
    labels = ['Original', 'Contrast', 'Brightness', 'Zoomed', 'Flipped', 'Rotated', 'Blurred', 'Distortion']

    point_pos = filename.rfind(".")
    filename_without_ext = filename[:point_pos]
    extension = filename[point_pos:]
    for i, image in enumerate(imgs):
        image_name = "./Image1002" + "_" + labels[i] +  extension
        cv.imwrite(image_name, image)





    plt.show()

    # for i in range (10):
    #     distortion = img_distortion(img, img.shape[0], img.shape[1])
    #     pcv.plot_image(distortion)


if __name__ == "__main__":
    main()


# Doc transformation :
# https://docs.opencv.org/3.4/da/d6e/tutorial_py_geometric_transformations.html
