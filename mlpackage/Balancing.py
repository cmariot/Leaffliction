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
import random


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


def get_max_files(path: str) -> int:

    """
    Return the maximum number of files in the subdirectories of a directory
    """

    max = -1
    for root, dir, files in os.walk(path):

        number_of_files = len(files)

        if number_of_files > max:
            max = number_of_files

    return max


def get_new_image_name(
    root: str, file: str, label: str,
    old_directory: str, new_directory: str
) -> str:

    new_root = root.replace(old_directory, new_directory, 1) + "/"
    point_position = file.rfind(".")
    if (point_position == -1):
        raise Exception("Invalid file name, no extension")
    if label:
        new_name = file[:point_position] + "_" + label + file[point_position:]
    else:
        new_name = file[:point_position] + file[point_position:]
    return new_root + new_name


class imageName():

    def __init__(self, full_name: str):
        r = full_name.rfind(".")
        if (r == -1):
            self.extension = None
            self.name = full_name
        else:
            self.extension = full_name[r + 1:]
            self.name = full_name[:full_name.rfind(".")]
        self.number = 0

    def get_name(self):
        if self.extension is None:
            if (self.number == 0):
                return self.name
            return self.name + "(" + str(self.number) + ")"
        else:
            if (self.number == 0):
                return self.name + "." + self.extension
            return str(
                self.name + "(" + str(self.number) + ")" + "." + self.extension
            )

    def increment(self):
        self.number += 1


def main():
    old_directory = parse_argument()
    augmentation_on_directory(old_directory, "augmented_directory", True)


def augmentation_on_directory(old_directory, new_directory, rac):

    if not os.path.isdir(old_directory):
        raise Exception("Invalid directory")

    slash_index = old_directory.rfind("/")

    if (slash_index == -1):
        old_directory_name = old_directory
    else:
        old_directory_name = old_directory[slash_index + 1:]

    print(new_directory)

    if rac:
        new_directory = "../" + new_directory + "/" + old_directory_name

    augmentedFunctions = {
        "Contrast": img_contrast,
        "Brightness": img_brightness,
        "Flip": img_flip,
        "Rotate": img_rotate,
        "Blur": img_blur
    }

    augmentations_labels = list(augmentedFunctions.keys())
    augmentation_functions = list(augmentedFunctions.values())

    to_balance = get_max_files(old_directory)

    new_directory = old_directory + "_augmented"
    print("new dir", new_directory)
    # if not os.path.isdir("../" + new_directory):
    #     os.mkdir("../" + new_directory)

    if not os.path.isdir(new_directory):
        print("Creating directory " + new_directory)
        os.mkdir(new_directory)

    for root, dirs, files in os.walk(old_directory):

        # Create the new directory structure
        for dir in dirs:
            if not os.path.isdir(new_directory + "/" + dir):
                os.mkdir(new_directory + "/" + dir)

        if (len(files) == 0):
            continue

        for file in files:
            img, path, filename = pcv.readimage(root + "/" + file)
            image_name = get_new_image_name(
                root, file, "", old_directory, new_directory
            )
            cv.imwrite(image_name, img)

        for i in range(to_balance - len(files)):

            file = files[i % len(files)]    # On ouvre notre image
            img, path, filename = pcv.readimage(root + "/" + file)
            random_number = random.randint(0, len(augmentedFunctions) - 1)
            augmented_image = augmentation_functions[random_number](img)
            label = augmentations_labels[random_number]

            image_name = get_new_image_name(
                root, file, label, old_directory, new_directory
            )
            new_filename = imageName(image_name)

            while os.path.isfile(new_filename.get_name()):
                new_filename.increment()
            image_name = new_filename.get_name()
            cv.imwrite(image_name, augmented_image)

            print(image_name)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit(1)
