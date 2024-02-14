import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from numpy import asarray
import sys
from Transformation import transform_image
from tensorflow import keras
import pickle


def get_class_name(image_path):
    splitted = image_path.split("/")
    if len(splitted) < 2:
        return image_path
    return splitted[-2]


if __name__ == "__main__":

    image_path = sys.argv[1]
    model_path = "model"
    list_transformations = [
        "Mask"
    ]

    # Load model
    model = keras.models.load_model(model_path)
    with open(f"{model_path}/class_names.pkl", "rb") as f:
        class_names = pickle.load(f)

    # Transformation de l'image
    images_transformed = transform_image(
        image_path,
        np.array(list_transformations),
        is_launch_on_dir=None,
        new_path=""
    )

    for key, image in images_transformed.items():

        x = np.expand_dims(image, axis=0)
        y_pred = model.predict(x)

        # Get the class names
        y_index = np.argmax(y_pred)
        y_hat = class_names[y_index]

        fig, axes = plt.subplots(1, 2)

        # Original image and transformed image
        axes[0].set_title("Original")
        axes[0].imshow(asarray(Image.open(image_path)))
        axes[0].axis('off')

        axes[1].set_title("Transformed")
        axes[1].imshow(image)
        axes[1].axis('off')

        y = get_class_name(image_path)

        if y in class_names:
            title = f"Class predicted: {y_hat}\nOriginal class: {y}"
            if y == y_hat:
                color = "green"
            else:
                color = "red"
        else:
            title = f"Class predicted: {y_hat}"
            color - 'black'

        plt.suptitle(
            title,
            fontsize=13,
            fontweight="bold",
            y=0.1,
            color=color
        )

        plt.show()
