import os


def path_to_name(path: str) -> str:

    """
    Return the name of the last directory in a path without the root,
    if the path is a file return the name of the file
    """

    car = path.rfind("/")
    if (car == -1):
        return path
    else:
        return path[car + 1:]


def count_files(path: str) -> dict:

    """
    Return a dictionary with the name of the directory as key
    and the number of files in the directory as value
    """

    data = {}
    for root, dirs, files in os.walk(path):
        key = path_to_name(root)
        number_of_files = len(files)
        if key in data:
            raise Exception("The name of the directory already exists")
        if number_of_files != 0:
            data[key] = number_of_files
    nb_files = sum(data.values())
    if nb_files == 0:
        raise Exception(f"The directory {path} is empty")
    print(f"\nTotal number of files in {path}: {nb_files}")
    return data
