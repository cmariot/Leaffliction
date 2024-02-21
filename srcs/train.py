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
        dir,
        train_dir,
        aug_dir,
        trans_dir,
        augmentation,
        transformation,
        model_path,
        epochs
    ) = parse_arguments()

    # print(f"Augmentation {augmentation}")
    # print(f"Transformation {transformation}")

    # if augmentation:
    #     print(f"Train directory: {train_dir}, will be used for augmentation")
    #     print(f"Augmented directory: {aug_dir}")
    #     train_dir = aug_dir

    # if transformation:
    #     print(f"{aug_dir} will be used for the transformation, and the result",
    #           f"will be saved in {trans_dir}"
    #           )
    #     train_dir = trans_dir

    # print(
    #     f"The training will be done on the {train_dir},",
    #     f"with original dir as {dir}"
    # )
    # exit()

    if augmentation:
        train_dir = augmentation_on_directory(train_dir)

    # tester -a avec dossier de test != nb d'images dans les dossiers ?
    if transformation:
        # train_dir = transform_directory(aug_dir, trans_dir, np.array(["Pseudolandmarks"]))
        train_dir = transform_directory(aug_dir, trans_dir, np.array(["Doublewithoutbg"]))
        # train_dir = transform_directory(aug_dir, trans_dir, np.array(["Mask"]))

    train(
        directory=train_dir,
        model_path=model_path,
        epochs=epochs,
        is_augmented=augmentation,
        is_transformed=transformation,
        original_dir=dir
    )

    zip_dir_list(
        dirs_list=[
            model_path,
            trans_dir
        ],
        output_filename="model.zip"
    )


if __name__ == "__main__":
    main()
    try:
        main()
    except Exception as error:
        print(error)
        exit(1)
