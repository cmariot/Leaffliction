import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
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


def predict_image(
    image_path,
    model,
    class_names,
    list_transformations,
    display_prediction=True
):

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

            gs = gridspec.GridSpec(2, 4)
            plt.figure(figsize=(16, 9))
            gs.update(wspace=0.5)

            ax1 = plt.subplot(gs[0, :2])
            ax2 = plt.subplot(gs[0, 2:])
            ax3 = plt.subplot(gs[1, 1:3])

            # Original image and transformed image
            ax1.set_title("Original image")
            ax1.imshow(asarray(Image.open(image_path)))
            ax1.axis('off')

            ax2.set_title("Transformed image used for prediction")
            ax2.imshow(image)
            ax2.axis('off')

            # Bar plot of the predictions probabilities
            ax3.set_title("Predictions probabilities for each class")
            ax3.barh(y=class_names, width=y_pred[0], height=0.2)
            ax3.set_yticks(range(len(class_names)))
            ax3.set_yticklabels(class_names)
            ax3.set_xlabel("Probability")
            ax3.set_ylabel("Class")
            ax3.set_xlim([0, 1])
            for i, v in enumerate(y_pred[0]):
                ax3.text(v, i, f"{v:.2f}", ha="left", va="center")

            if y in class_names:

                title = f"Class predicted: {y_hat}\nOriginal class: {y}"
                if y == y_hat:
                    color = "green"
                else:
                    color = "red"

            else:

                title = f"Class predicted: {y_hat}"
                color = 'black'

            # Title at the Axes[1, 1] position
            plt.suptitle(
                title,
                y=0.95,
                fontsize=13,
                fontweight="bold",
                ha="center",
                va="center",
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

            if not os.path.isfile(image_path):
                print(f"The file {image_path} does not exist.")
                continue

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
                    plt.close()
                    continue
                else:
                    break

            print(f"Accuracy: {correct_predictions / total_predictions}")

    else:

        image_path = sys.argv[1]
        predict_image(
            image_path,
            model,
            class_names,
            list_transformations,
            display_prediction=True
        )
