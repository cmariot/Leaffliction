def get_new_image_name(
    root: str, file: str, label: str,
    old_directory: str, new_directory: str
) -> str:

    new_root = root.replace(old_directory, new_directory, 1) + "/"
    point_position = file.rfind(".")
    if (point_position == -1):
        raise Exception("Invalid file name, no extension")
    if label:
        new_name = file[:point_position] + "_" + label + file[point_position:]
    else:
        new_name = file[:point_position] + file[point_position:]
    return new_root + new_name
