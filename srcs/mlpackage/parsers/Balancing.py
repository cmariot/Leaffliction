import argparse
import os


def parse_argument() -> str:

    """
    Parse the argument of the program,
    return the path of the directory to analyze
    """

    parser = argparse.ArgumentParser(
        prog='Distribution',
        description="Distribution of files in a directory",
        epilog='----'
    )
    parser.add_argument('folder')
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        raise Exception("Invalid directory")

    return args.folder
