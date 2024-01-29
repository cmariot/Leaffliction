import argparse
from plantcv import plantcv as pcv
import random
import os
import numpy as np


def parse_argument():
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument('filename')
    args = parser.parse_args()
    return args.filename


def main():

    filename = parse_argument()

    if not os.path.exists(filename):
        raise Exception("The path does not exist")
    elif not os.path.isfile(filename):
        raise Exception("The path is not a file")

    img, path, name = pcv.readimage(filename)

    # Flip image vertically
    flipped = pcv.flip(img, "vertical")

    # Rotate image by a random degree between 0 and 360
    rotated = pcv.transform.rotate(img, random.randint(0, 360), crop=False)

    # Blur image
    blurred = pcv.gaussian_blur(img, (5, 5), 1)

    # Crop
    img_height, img_width, _ = np.shape(img)
    x = random.randint(0, int(img_width * 0.25))
    # y = random.randint((img_height * 0.25))
    y = int(x * img_height / img_width)


    # ratio = img_height / img_width

    # w = img_width / 100 * random.randint(0, 100)
    # h = random.randint(0, 100)
    pcv.plot_image(img)
    cropped = pcv.crop(img, x, y, int(img_width / 2), int(img_height / 2))
    pcv.plot_image(cropped)
    cropped = pcv.transform.resize(img=cropped, size=(img_width, img_height))

    # Projective transform
    # transform_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    # projection = pcv.transform.apply_transformation_matrix(
    #     img,
    #     img,
    #     transform_matrix,
    # )


    # pcv.plot_image(img)
    # pcv.plot_image(flipped)
    # pcv.plot_image(rotated)
    # pcv.plot_image(blurred)
    pcv.plot_image(cropped)
    # pcv.plot_image(projection)


if __name__ == "__main__":
    main()


# Doc transformation :
# https://docs.opencv.org/3.4/da/d6e/tutorial_py_geometric_transformations.html
