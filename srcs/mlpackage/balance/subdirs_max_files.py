import os


def subdirs_max_files(path: str) -> int:

    """
    Return the maximum number of files in the subdirectories of a directory
    """

    max = -1

    for root, dir, files in os.walk(path):
        number_of_files = len(files)

        if number_of_files > max:
            max = number_of_files

    if max <= 0:
        raise Exception(f"The directory {path} is empty")

    return max
