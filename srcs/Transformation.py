from mlpackage.parsers.Transformation import parse_argument
from mlpackage.image_transformation.transform_image import transform_image
from mlpackage.image_transformation.transform_directory \
    import transform_directory
from mlpackage.colors_variable import GREEN, RESET
import os


def intro() -> None:
    print(
        f"""{GREEN}
 _____                     __                            _   _
|_   _| __ __ _ _ __  ___ / _| ___  _ __ _ __ ___   __ _| |_(_) ___  _ __
  | || '__/ _` | '_ \\/ __| |_ / _ \\| '__| '_ ` _ \\ / _` | __| |/ _ \\| '_ \\
  | || | | (_| | | | \\__ \\  _| (_) | |  | | | | | | (_| | |_| | (_) | | | |
  |_||_|  \\__,_|_| |_|___/_|  \\___/|_|  |_| |_| |_|\\__,_|\\__|_|\\___/|_| |_|

{RESET}\n""" +
        "This program displays the original image and the transformed images.\n"
        "The transformed images are saved in the same directory as the",
        "original image.\n"
    )


def main():

    """
    Main function of the program,
    it calls the other functions depending on the path
    - If the path is a file, display the transformation of the image.
    - If the path is a directory, save the transformation of all the images
    """

    intro()

    # path : path of the directory to transform
    # dest : destination path, where the transformations will be saved
    # options : which transformations apply
    path, dest, options = parse_argument()

    if os.path.isfile(path):
        transform_image(path, options)
    elif os.path.isdir(path):
        transform_directory(path, dest, options)
    else:
        raise Exception("The path is not a file or a directory")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSIGTERM")
        exit()
    except Exception as error:
        print(error)
        exit(1)
