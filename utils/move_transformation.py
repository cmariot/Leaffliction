import pickle
import os

if __name__ == "__main__":

    valpath_file = "model_reverse_with_valpath94.40/validation_paths.pkl"
    previous_path = "images"
    new_path = "/media/cmariot/VM/images"

    list_valpath = pickle.load(open(valpath_file, "rb"))

    new_paths = []
    for path in list_valpath:
        # path = path.replace(previous_path, new_path, 1)
        slash_index = path.rfind("/")
        if slash_index != -1:
            filename = path[slash_index + 1:]
        extension_index = path.rfind(".")
        extension = path[extension_index:]
        for i in range(2):
            underscore_index = filename.rfind("_")
            if underscore_index == -1:
                break
            else:
                filename = filename[:underscore_index]
            path = path[:slash_index + 1] + filename
        path = path + extension
        print(path)
        new_paths.append(path)

    os.rename(valpath_file, valpath_file + ".bak")
    with open(valpath_file, "wb") as valpath_file:
        pickle.dump(new_paths, valpath_file)
