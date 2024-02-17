from parsers.Balancing import parse_argument
import os
import cv2 as cv
from plantcv import plantcv as pcv
import random
from image_augmentation.ImageAugmentation import ImageAugmentation


def subdirs_max_files(path: str) -> int:

    """
    Return the maximum number of files in the subdirectories of a directory
    """

    max = -1

    for root, dir, files in os.walk(path):
        number_of_files = len(files)

        if number_of_files > max:
            max = number_of_files

    if max <= 0:
        raise Exception(f"The directory {path} is empty")

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


def warning_dir_exists(new_directory):

    print(
        f"Warning, the directory {new_directory} already exists.",
        "Balancing in this directory may append a wrong number of files."
    )

    while (1):

        need_delete_dir = input(
            f"Do you want to remove the existing {new_directory} ? (y/n) "
        )

        if need_delete_dir == "y":

            for root, dirs, files in os.walk(new_directory, topdown=False):

                for file in files:
                    os.remove(os.path.join(root, file))

                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))

            if os.path.isdir(new_directory):
                os.rmdir(new_directory)

            print(
                f"The directory {new_directory} has been successfully",
                "deleted, it will be rectreated with new augmented images"
            )
            break
        elif need_delete_dir == "n":
            print(
                f"Anyway, new images will be added to {new_directory}"
            )
            break
        else:
            print(
                "Invalid input, type 'y' or 'n'."
            )
            continue


def augmentation_on_directory(old_directory):

    augmentedFunctions = {
        "Contrast": ImageAugmentation.contrast,
        "Brightness": ImageAugmentation.brightness,
        "Flip": ImageAugmentation.flip,
        "Rotate": ImageAugmentation.rotate,
        "Blur": ImageAugmentation.blur,
    }

    augmentations_labels = list(augmentedFunctions.keys())
    augmentation_functions = list(augmentedFunctions.values())

    to_balance = subdirs_max_files(old_directory)

    new_directory = old_directory + "_augmented"

    if os.path.isdir(new_directory):
        warning_dir_exists(new_directory)

    if not os.path.isdir(new_directory):
        os.makedirs(new_directory)

    for root, dirs, files in os.walk(old_directory):

        for dir in dirs:
            if not os.path.isdir(os.path.join(new_directory, dir)):
                os.makedirs(os.path.join(new_directory, dir))

        if len(files) == 0:
            continue

        for file in files:

            img = ImageAugmentation.read_image(root + "/" + file)
            image_name = get_new_image_name(
                root, file, "", old_directory, new_directory
            )
            cv.imwrite(image_name, img)

        for i in range(to_balance - len(files)):

            file = files[i % len(files)]
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


def main():
    old_directory = parse_argument()
    augmentation_on_directory(old_directory)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit(1)
