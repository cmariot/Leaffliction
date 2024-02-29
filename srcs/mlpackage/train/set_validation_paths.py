def set_validation_paths(
    val_ds,
    is_augmented,
    is_transformed,
    transformation_dir: str,
    original_dir
):

    """
    Transform the validation paths to the original paths
    Will be saved in a pickle file, used for the prediction
    """

    if not is_transformed and not is_augmented:
        return val_ds.file_paths

    if transformation_dir[-1] == "/":
        transformation_dir = transformation_dir[:-1]

    validation_paths_lst = []
    for path in val_ds.file_paths:
        path = path.replace(transformation_dir, original_dir, 1)
        slash_index = path.rfind("/")
        if slash_index != -1:
            filename = path[slash_index + 1:]
        extension_index = path.rfind(".")
        extension = path[extension_index:]
        for i in range(is_augmented + is_transformed):
            underscore_index = filename.rfind("_")
            if underscore_index == -1:
                break
            else:
                filename = filename[:underscore_index]
            path = path[:slash_index + 1] + filename
        path = path + extension
        validation_paths_lst.append(path)
    return validation_paths_lst
