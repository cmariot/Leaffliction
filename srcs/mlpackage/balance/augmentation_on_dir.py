import os
import cv2 as cv
import random
from plantcv import plantcv as pcv

from .subdirs_max_files import subdirs_max_files
from .warning_dir_exists import warning_dir_exists
from .ImageName import ImageName
from ..distribution.print_directory_structure import print_directory_structure
from ..image_augmentation.ImageAugmentation import ImageAugmentation
from .get_new_image_name import get_new_image_name


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

    GREEN = "\033[92m"
    RESET = "\033[0m"
    print(
        f"{GREEN}" +
        f"Augmentation phase, creating {new_directory} " +
        f"from {old_directory}:{RESET}\n"
    )

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

        print(f" - Augmentation of {GREEN}{root}{RESET}")

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
            new_filename = ImageName(image_name)

            while os.path.isfile(new_filename.get_name()):
                new_filename.increment()

            image_name = new_filename.get_name()
            cv.imwrite(image_name, augmented_image)

    print()
    print_directory_structure(new_directory)
    print()

    return old_directory + "_augmented/"
