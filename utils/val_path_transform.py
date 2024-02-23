import pickle
import os
import sys


if __name__ == "__main__":

    if len(sys.argv) < 4:
        print(
            "Usage: python val_path_transform.py <validation_paths.pkl>" +
            "<previous path> <new path>"
        )
        exit(1)

    # Load the validation paths from the pickle file
    with open(sys.argv[1], "rb") as f:
        validation_paths = pickle.load(f)

    # Print the paths
    new_paths = []

    for path in validation_paths:
        path = path.replace(sys.argv[2], sys.argv[3])
        new_paths.append(path)
        print(path)

    # Rm the old paths file if it exists
    try:
        os.remove(sys.argv[1])
    except FileNotFoundError:
        pass

    # Save the new paths to a pickle file
    with open(sys.argv[1], "wb") as f:
        pickle.dump(new_paths, f)