import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from numpy import asarray
import sys
import os
sys.path.insert(1, '/media/cmariot/VM/Leaffliction//transformation')
from Transformation import transform_image
from tensorflow import keras
import pickle



def get_class_name(image_path):
    return image_path.split("/")[-2]


if __name__ == "__main__":

    image_path = sys.argv[1]
    model_path = "model"

    # Load model
    # model = tf.saved_model.load("model")
    model = keras.models.load_model(model_path)
    # print(model.layers[-1].vocab)

    list_transformations = [
        "Mask"
    ]

    # Transformation de l'image
    images_transformed = transform_image(
        image_path,
        np.array(list_transformations),
        is_launch_on_dir=None,
        new_path=""
    )

    with open(f"{model_path}/class_names.pkl", "rb") as f:
        class_names = pickle.load(f)

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

        if y == y_hat:
            color = "green"
        else:
            color = "red"

        plt.suptitle(
            f"Class predicted: {y_hat}\nOriginal class: {y}",
            fontsize=13,
            fontweight="bold",
            y=0.1,
            color=color
        )

        plt.show()

    exit()



    # Predict
    nb_apples = 0
    total = 0
    for root, dirs, files in os.walk(image_path):
        for file in files:

            image_path = os.path.join(root, file)
            image = asarray(Image.open(image_path))
            x = np.expand_dims(image, axis=0)
            y_pred = model.predict(x)

            # Get the class names
            y_index = np.argmax(y_pred)
            class_names = ["Apple", "Grape"]
            y_hat = class_names[y_index]

            if y_index == 1:
                nb_apples += 1
            # plt.title(sys.argv[1] + " Predicted " + y_hat)
            # plt.imshow(image)
            # plt.show()
            total += 1

    print("Number of apples : ", nb_apples)
    print("Total images : ", total)
    exit()
