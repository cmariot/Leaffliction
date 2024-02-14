import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from numpy import asarray
import sys
from Transformation import transform_image
from tensorflow import keras
import pickle
import os


def get_class_name(image_path):
    splitted = image_path.split("/")
    if len(splitted) < 2:
        return image_path
    return splitted[-2]


def predict_image(image_path, model, class_names, list_transformations, display_prediction=True):

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
        y_pred = model.predict(x)

        # Get the class names
        y_index = np.argmax(y_pred)
        y_hat = class_names[y_index]

        y = get_class_name(image_path)

        if y == y_hat:
            correct += 1

        print(f"Predicted class: {y_hat}")
        print(f"Original class: {y}")

        if display_prediction:

            fig, axes = plt.subplots(1, 2)

            # Original image and transformed image
            axes[0].set_title("Original")
            axes[0].imshow(asarray(Image.open(image_path)))
            axes[0].axis('off')

            axes[1].set_title("Transformed")
            axes[1].imshow(image)
            axes[1].axis('off')

            if y in class_names:

                title = f"Class predicted: {y_hat}\nOriginal class: {y}"
                if y == y_hat:
                    color = "green"
                else:
                    color = "red"

            else:

                title = f"Class predicted: {y_hat}"
                color = 'black'

            plt.suptitle(
                title,
                fontsize=13,
                fontweight="bold",
                y=0.1,
                color=color
            )

            plt.show()
            # plt.savefig(f"{key}.png")
            plt.close()

    return correct / len(images_transformed)


if __name__ == "__main__":

    model_path = "model"
    list_transformations = [
        "Mask"
    ]

    # Load model
    model = keras.models.load_model(model_path)
    with open(f"{model_path}/class_names.pkl", "rb") as f:
        class_names = pickle.load(f)

    if len(sys.argv) < 2:

        with open(f"{model_path}/validation_paths.pkl", "rb") as f:
            validation_paths = pickle.load(f)

        correct_predictions = 0
        total_predictions = 0
        display_prediction = True

        for image_path in validation_paths:
            try:
                correct_predictions += predict_image(
                    image_path,
                    model,
                    class_names,
                    list_transformations,
                    display_prediction
                )
                total_predictions += 1
            except KeyboardInterrupt:
                if display_prediction:
                    display_prediction = False
                    continue
                else:
                    break

            print(f"Accuracy: {correct_predictions / total_predictions}")

    else:

        image_path = sys.argv[1]
        predict_image(image_path, model, list_transformations)
