import os


GREEN = '\033[92m'
RESET = '\033[0m'


def print_directory_structure(path: str):

    """

    Print the structure of the directory with the number of files in each
    directory.

    Example:

    images
        Grape_Esca: 1382 files
        Grape_healthy: 422 files
        Apple_scab: 629 files
        Grape_Black_rot: 1178 files
        Apple_healthy: 1640 files
        Grape_spot: 1075 files
        Apple_rust: 275 files
        Apple_Black_rot: 620 files

    """

    for root, _, files in os.walk(path):

        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)

        dir_name = os.path.basename(root)
        nb_files = len(files)

        if nb_files != 0:
            print(f'{indent}{dir_name}: {GREEN}{nb_files}{RESET} files')
        else:
            print(f'{indent}{dir_name}')
