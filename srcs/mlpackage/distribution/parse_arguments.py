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
    )
    parser.add_argument('path')
    args = parser.parse_args()
    if not os.path.isdir(args.path):
        raise Exception(
            f"The path given as argument, ({args.path}), is not a directory"
        )
    return args.path
