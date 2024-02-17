import argparse
import os


def parse_argument():

    parser = argparse.ArgumentParser(
        prog='Augmentation',
        description='This program displays the original' +
        'image and the augmented images.'
    )

    parser.add_argument('filename')
    args = parser.parse_args()
    filename = args.filename

    if not os.path.exists(filename):
        raise Exception(f"{filename} does not exist")
    elif not os.path.isfile(filename):
        raise Exception(f"{filename} is not a file")

    return filename
