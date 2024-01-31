import os
import argparse
import cv2 as cv
from plantcv import plantcv as pcv
from Augmentation import (
    img_contrast,
    img_brightness,
    img_flip,
    img_rotate,
    img_blur
)


def parse_argument() -> str:

    """
    Parse the argument of the program,
    return the path of the directory to analyze
    """

    parser = argparse.ArgumentParser(
                    prog='Distribution',
                    description="Distribution of files in a directory",
                    epilog='----')
    parser.add_argument('folder')
    args = parser.parse_args()
    return args.folder


def main():

    augmentedFunctions = {
        "Contrast": img_contrast,
        "Brightness": img_brightness,
        "Flip": img_flip,
        "Rotate": img_rotate,
        "Blur": img_blur
    }

    old_directory = "../images"
    new_directory = "../augmented_directory"

    # folder = parse_argument()

    if not os.path.isdir(new_directory):
        os.mkdir(new_directory)

    for root, dirs, files in os.walk(old_directory):

        # Create the new directory structure
        for dir in dirs:
            if not os.path.isdir(new_directory + "/" + dir):
                os.mkdir(new_directory + "/" + dir)

        for file in files:

            for label, func in augmentedFunctions.items():
                img, path, name = pcv.readimage(os.path.join(root, file))
                augmented_image = func(img)

                last_slash_position = root.rfind("/")
                if (last_slash_position == -1):
                    raise Exception("Invalid root name, no / character wtf")
                subdirectory = root[last_slash_position:] + "/"
                extension = file[-4:]
                image_name = new_directory + \
                    subdirectory + \
                    file[:-4] + "_" + label + \
                    extension

                cv.imwrite(image_name, augmented_image)

                print(image_name)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit(1)
