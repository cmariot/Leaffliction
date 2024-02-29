import os


def warning_dir_exists(new_directory):

    print(
        f"Warning, the directory {new_directory} already exists.",
        "Balancing in this directory may append a wrong number of files."
    )

    while (1):

        need_delete_dir = input(
            f"Do you want to remove the existing {new_directory} ? (y/n) "
        )

        if need_delete_dir == "y":

            for root, dirs, files in os.walk(new_directory, topdown=False):

                for file in files:
                    os.remove(os.path.join(root, file))

                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))

            if os.path.isdir(new_directory):
                os.rmdir(new_directory)

            print(
                f"The directory {new_directory} has been successfully",
                "deleted, it will be rectreated with new augmented images"
            )
            break
        elif need_delete_dir == "n":
            print(
                f"Anyway, new images will be added to {new_directory}"
            )
            break
        else:
            print(
                "Invalid input, type 'y' or 'n'."
            )
            continue

    print()
