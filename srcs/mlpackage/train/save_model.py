from pickle import dump


def save_model(model, model_path, train_class_names, validation_paths_lst):

    """
    Save the trained model and the class names
    """

    model.save(model_path)

    with open(model_path + "/class_names.pkl", "wb") as f:
        dump(train_class_names, f)

    with open(model_path + "/validation_paths.pkl", "wb") as f:
        dump(validation_paths_lst, f)

    print("Model saved at : ", model_path)