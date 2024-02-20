import argparse
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
        "--epochs", "-e",
        type=int,
        default=10,
        help="Number of epochs for the training"
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

    parser.add_argument(
        "--model_path", "-m",
        type=str,
        default="model",
        help="The path where the model will be saved"
    )

    args = parser.parse_args()

    # Check if the directory exists
    if not os.path.isdir(args.dir):
        raise Exception("The directory given as argument does not exist")

    # Remove the last / in dir if it exists
    if len(args.dir) > 0 and args.dir[-1] == "/":
        args.dir = args.dir[:-1]

    return (
        args.dir,
        not args.augmentation,
        not args.transformation,
        args.model_path,
        args.epochs
    )
