import os
import zipfile


def remove_directory(directory):

    """
    Remove a directory and its content
    """

    if not os.path.isdir(directory):
        raise Exception(f"Can't remove {directory}, it doesn't exist.")

    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))

    os.rmdir(directory)


def zip_dir_list(dirs_list, aug_dir, output_filename):

    """
    Zip a list of directories and remove them
    + remove the augmented directory (without zip it)
    """

    with zipfile.ZipFile(
        output_filename, 'w', zipfile.ZIP_DEFLATED
    ) as zip_file:
        for directory in dirs_list:
            if not os.path.exists(directory):
                continue
            for root, _, files in os.walk(directory):
                for file in files:
                    zip_file.write(
                        os.path.join(root, file),
                    )
            remove_directory(directory)
        remove_directory(aug_dir)
