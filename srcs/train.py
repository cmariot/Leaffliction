import argparse
from mlpackage.Balancing import augmentation_on_directory
from Transformation import transform_directory
from mlpackage.Fit import train
import numpy as np
import os


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

    # Check if the directory exists
    if not os.path.isdir(args.dir):
        raise Exception("The directory given as argument does not exist")

    # Revome the last / in dir if it exists
    if len(args.dir) > 0 and args.dir[-1] == "/":
        args.dir = args.dir[:-1]

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



    train_dir = dir
    aug_dir = dir + "_augmented/"
    trans_dir = dir + "_transformed/"

    if augmentation:
        augmentation_on_directory(dir, aug_dir, False)
        train_dir = aug_dir
    else:
        aug_dir = dir

    if transformation:
        transform_directory(aug_dir, trans_dir, np.array(["Pseudolandmarks"]))
        train_dir = trans_dir

    train(train_dir, "model", 1000)


if __name__ == "__main__":
    main()
    exit()
    try:
        main()
    except Exception as error:
        print(error)
        exit(1)
