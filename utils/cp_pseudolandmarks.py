import os
import shutil


if __name__ == "__main__":

    file_to_move = "_Pseudolandmarks.JPG"
    srcs = "/media/cmariot/VM/images_transformed"
    dest = "/media/cmariot/VM/pseudolandmarks"

    if not os.path.isdir(dest):
        print(f"Creation of the {dest} directory")
        os.makedirs(dest)

    for root, dirs, files in os.walk(srcs):

        new_root = root.replace(srcs, dest, 1)
        print(f"New root : {new_root}")

        for dir in dirs:
            dirpath = os.path.join(new_root, dir)
            if not os.path.isdir(dirpath):
                os.makedirs(dirpath)

        for file in files:
            filepath = os.path.join(root, file)
            new_filepath = os.path.join(new_root, file)
            if filepath.endswith(file_to_move):
                shutil.copy(filepath, new_filepath)
