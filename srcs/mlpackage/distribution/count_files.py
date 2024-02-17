import os


GREEN = "\033[92m"
RESET = "\033[0m"


def count_files(path: str) -> dict:

    """
    Return a dictionary with the name of the directory as key
    and the number of files in the directory as value
    """

    dirs_dict = {}

    for root, _, files in os.walk(path):

        last_dir = os.path.basename(root)
        number_of_files = len(files)

        if last_dir in dirs_dict:
            raise Exception(
                f"The directory {last_dir} is present in the " +
                f"path {path} more than once"
            )

        if number_of_files != 0:
            dirs_dict[last_dir] = number_of_files

    nb_files = sum(dirs_dict.values())
    if nb_files == 0:
        raise Exception(f"The directory {path} is empty")

    print(f"\nTotal number of files in {path}: {GREEN}{nb_files}{RESET}")

    return dirs_dict
