import os
import keras
import pickle


def load_model(model_path: str, is_predict_validation_set: bool) -> tuple:

    """
    Load the trained model used to make predictions
    if is_predict_validation_set is True, the predictions will be done in a loop
    for each element of the validation set, need to load the paths
    """

    if not os.path.isdir(model_path):
        raise ValueError(f"The model path {model_path} does not exist.")
    if not os.path.isfile(f"{model_path}/class_names.pkl"):
        raise ValueError(
            f"The file {model_path}/class_names.pkl does not exist."
        )
    model = keras.models.load_model(model_path)
    with open(f"{model_path}/class_names.pkl", "rb") as f:
        class_names = pickle.load(f)
    if is_predict_validation_set:
        if not os.path.isfile(f"{model_path}/validation_paths.pkl"):
            raise ValueError(
                f"The file {model_path}/validation_paths.pkl does not exist."
            )
        with open(f"{model_path}/validation_paths.pkl", "rb") as f:
            validation_paths = pickle.load(f)
    else:
        validation_paths = None
    return (model, class_names, validation_paths)
