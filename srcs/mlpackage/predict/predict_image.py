import numpy as np
from ..image_transformation.transform_image import transform_image
from .plot_prediction import plot_prediction
from ..colors_variable import GREEN, RESET


def get_class_name(image_path):
    splitted = image_path.split("/")
    if len(splitted) < 2:
        return image_path
    return splitted[-2]


def predict_image(
    image_path,
    model,
    class_names,
    list_transformations,
    display_prediction=True
):

    print(f"Predicting image: {GREEN}{image_path}{RESET}")

    # Transformation de l'image
    images_transformed = transform_image(
        image_path,
        np.array(list_transformations),
        is_launch_on_dir=None,
        new_path=""
    )

    correct = 0

    for key, image in images_transformed.items():

        x = np.expand_dims(image, axis=0)
        y_pred = model.predict(x, verbose=0)

        # Get the class names
        y_index = np.argmax(y_pred)
        y_hat = class_names[y_index]

        y = get_class_name(image_path)

        if y == y_hat:
            correct += 1

        print(f"Predicted class: {y_hat}")
        print(f"Original class: {y}")

        if display_prediction:
            plot_prediction(
                y,
                y_hat,
                y_pred,
                class_names,
                image,
                image_path
            )

    return correct / len(images_transformed)
