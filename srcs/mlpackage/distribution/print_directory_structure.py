import os


def print_directory_structure(path: str):

    """
    Print the structure of the directory
    """

    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        dir_name = os.path.basename(root)
        nb_files = len(files)
        if nb_files != 0:
            print(f'{indent}{dir_name}: {nb_files} files')
        else:
            print(f'{indent}{dir_name}')
