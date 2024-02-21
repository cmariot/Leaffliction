import os
from tqdm import tqdm
from .transform_image import transform_image


def transform_directory(path, dest, options):

    """
    Transform all the images in the directory 'path' and save them in the
    'dest' directory
    """

    if not os.path.isdir(dest):
        os.makedirs(dest)

    GREEN = "\033[92m"
    RESET = "\033[0m"
    print(f"{GREEN}Transformation phase, creating {dest} from {path}:\n{RESET}")

    for root, dirs, files in os.walk(path):

        new_root = root.replace(path, dest, 1)

        for dir in dirs:
            if not os.path.isdir(os.path.join(new_root, dir)):
                os.makedirs(os.path.join(new_root, dir))

        print(f"Transformation of (root) {root}")

        for file in tqdm(files):
            full_path = os.path.join(root, file)
            new_path = os.path.join(new_root, file)
            transform_image(
                full_path,
                options,
                is_launch_on_dir=True,
                new_path=new_path
            )

    return dest
