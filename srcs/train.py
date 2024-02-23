from mlpackage.Balancing import augmentation_on_directory
from Transformation import transform_directory
from mlpackage.Fit import train
import numpy as np
from mlpackage.parsers.train import parse_arguments
from mlpackage.colors_variable import GREEN, RESET
from mlpackage.utils.zip_dir import zip_dir_list


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
        dir, train_dir, aug_dir, trans_dir,
        augmentation, transformation,
        model_path,
        epochs,
        need_zip
    ) = parse_arguments()

    if augmentation:
        train_dir = augmentation_on_directory(train_dir)

    if transformation:
        train_dir = transform_directory(
            aug_dir, trans_dir, np.array(["Doublewithoutbg"])
        )

    train(
        directory=train_dir,
        model_path=model_path,
        epochs=epochs,
        is_augmented=augmentation,
        is_transformed=transformation,
        original_dir=dir
    )

    if need_zip:
        zip_dir_list(
            dirs_list=[
                model_path,
                trans_dir
            ],
            aug_dir=aug_dir,
            output_filename=model_path + ".zip"
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
        exit(1)
