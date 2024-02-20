from mlpackage.Balancing import augmentation_on_directory
from Transformation import transform_directory
from mlpackage.Fit import train
import numpy as np
from mlpackage.parsers.train import parse_arguments
from mlpackage.colors_variable import GREEN, RESET
from mlpackage.utils.zip_dir import zip_dir


def intro():
    print(
        f"""{GREEN}
 _____          _
|_   _| __ __ _(_)_ __
  | || '__/ _` | | '_ \\
  | || | | (_| | | | | |
  |_||_|  \\__,_|_|_| |_|
{RESET}\n""" +
        "This program will train a model on the given directory\n" +
        "It will apply augmentation and transformation to the dataset\n" +
        "The model will be saved in the model directory\n"
    )


def main():

    intro()

    (
        dir,
        augmentation,
        transformation,
        model_path
    ) = parse_arguments()

    train_dir = dir
    aug_dir = dir + "_augmented/"
    trans_dir = dir + "_transformed/"

    if augmentation:
        augmentation_on_directory(dir, aug_dir)
        train_dir = aug_dir
    else:
        aug_dir = dir

    if transformation:
        transform_directory(aug_dir, trans_dir, np.array(["Pseudolandmarks"]))
        train_dir = trans_dir

    train(
        directory=train_dir,
        model_path=model_path,
        epochs=1000,
        is_augmented=augmentation,
        is_transformed=transformation,
        original_dir=dir
    )

    # Zip the directory containing :
    # - model
    # - images_augmented
    # - images_transformed
    zip_dir(model_path, trans_dir, "model.zip")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
        exit(1)
