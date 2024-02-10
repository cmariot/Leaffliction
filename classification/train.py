import argparse
from Balancing import augmentation_on_directory
from Transformation import transform_directory
from Fit import train
import numpy as np


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


# Augmentation
# Transformation
# Model
# Training
# Evaluation
# Save model


def main():

    (
        dir,
        augmentation,
        transformation,
        rm_augmentation,
        rm_transformation
    ) = parse_arguments()

    train_dir = dir
    aug_dir = "minifitaug/"
    trans_dir = "minifitrans/"

    if augmentation:
        augmentation_on_directory(dir, aug_dir, False)
        train_dir = aug_dir
    else:
        aug_dir = dir

    if transformation:
        transform_directory(aug_dir, trans_dir, np.array(["Mask"]))
        train_dir = trans_dir

    train(train_dir, "model", 2)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit(1)
