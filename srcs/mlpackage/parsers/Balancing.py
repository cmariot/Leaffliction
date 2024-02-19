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

    directory_path = args.folder

    # Remove the last / in dir if it exists
    if len(directory_path) > 0 and directory_path[-1] == "/":
        directory_path = directory_path[:-1]

    if not os.path.isdir(directory_path):
        raise Exception("Invalid directory")

    return directory_path
