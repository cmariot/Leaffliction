import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from numpy import asarray
import sys
from Transformation import transform_image
from tensorflow import keras
import pickle
<<<<<<< HEAD
import os
=======

>>>>>>> 61e0272355785fb3ec02a1728b7d5531bfa8780b

def get_class_name(image_path):
    splitted = image_path.split("/")
    if len(splitted) < 2:
        return image_path
    return splitted[-2]


<<<<<<< HEAD
def predict_image(image_path, model_path, list_transformations):

    # Load model
    model = keras.models.load_model(model_path)
    with open(f"{model_path}/class_names.pkl", "rb") as f:
        class_names = pickle.load(f)
=======
if __name__ == "__main__":

    image_path = sys.argv[1]
    model_path = "model"
    list_transformations = [
        "Mask"
    ]
>>>>>>> 61e0272355785fb3ec02a1728b7d5531bfa8780b

    # Load model
    model = keras.models.load_model(model_path)
    with open(f"{model_path}/class_names.pkl", "rb") as f:
        class_names = pickle.load(f)

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

<<<<<<< HEAD
<<<<<<< HEAD
    correct = 0

=======
>>>>>>> 61e0272355785fb3ec02a1728b7d5531bfa8780b
=======
>>>>>>> 61e0272355785fb3ec02a1728b7d5531bfa8780b
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
<<<<<<< HEAD
<<<<<<< HEAD
            color = 'black'
=======
            color - 'black'
>>>>>>> 61e0272355785fb3ec02a1728b7d5531bfa8780b
=======
            color - 'black'
>>>>>>> 61e0272355785fb3ec02a1728b7d5531bfa8780b

        plt.suptitle(
            title,
            fontsize=13,
            fontweight="bold",
            y=0.1,
            color=color
        )

<<<<<<< HEAD
        # plt.show()
        plt.savefig(f"{key}.png")

        if y == y_hat:
            correct += 1

    return correct / len(images_transformed)


if __name__ == "__main__":

    image_path = sys.argv[1]
    model_path = "model"
    list_transformations = [
        "Mask"
    ]

    if os.path.isdir(image_path):

        correct = 0
        total = 0
        for root, dirs, files in os.walk(image_path):
            for file in files:
                image_path = os.path.join(root, file)
                correct += predict_image(
                    image_path,
                    model_path,
                    list_transformations
                )
                total += 1
        print(f"Accuracy: {correct / total}")

    else:
        predict_image(image_path, model_path, list_transformations)
=======
        plt.show()
<<<<<<< HEAD
>>>>>>> 61e0272355785fb3ec02a1728b7d5531bfa8780b
=======
>>>>>>> 61e0272355785fb3ec02a1728b7d5531bfa8780b
