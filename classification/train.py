import argparse
from Balancing import augmentation_on_directory
from Transformation import transform_directory
from Fit import train
import numpy as np
<<<<<<< HEAD
<<<<<<< HEAD
import os
=======
>>>>>>> 61e0272355785fb3ec02a1728b7d5531bfa8780b
=======
>>>>>>> 61e0272355785fb3ec02a1728b7d5531bfa8780b


def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Train a classification model"
    )

    parser.add_argument(
        "dir",
        type=str,
    )

    parser.add_argument(
        "--augmentation", "-a",
        action="store_true",
        help="Don't apply augmentation to the dataset"
    )

    parser.add_argument(
        "--transformation", "-t",
        action="store_true",
        help="Don't apply transformation to the dataset"
    )

    args = parser.parse_args()

    return (
        args.dir,
        not args.augmentation,
        not args.transformation
    )


def main():

    (
        dir,
        augmentation,
        transformation
    ) = parse_arguments()
<<<<<<< HEAD
<<<<<<< HEAD

    # Check if the directory exists
    if not os.path.isdir(dir):
        raise Exception("The directory does not exist")
=======
>>>>>>> 61e0272355785fb3ec02a1728b7d5531bfa8780b
=======
>>>>>>> 61e0272355785fb3ec02a1728b7d5531bfa8780b

    train_dir = dir
    aug_dir = dir + "_augmented/"
    trans_dir = dir + "_transformed/"

    if augmentation:
        augmentation_on_directory(dir, aug_dir, False)
        train_dir = aug_dir
    else:
        aug_dir = dir

    if transformation:
        transform_directory(aug_dir, trans_dir, np.array(["Mask"]))
        train_dir = trans_dir

    train(train_dir, "model", 10)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
        exit(1)
