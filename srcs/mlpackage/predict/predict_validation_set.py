import os
from .predict_image import predict_image
import matplotlib.pyplot as plt
from ..colors_variable import RED, RESET


def predict_validation_set(
    validation_paths: list,
    model,
    class_names,
    list_transformations
):

    correct_predictions = 0
    total_predictions = 0
    display_prediction = True

    for image_path in validation_paths:

        if not os.path.isfile(image_path):
            print(
                f"{RED}Warning:{RESET} The file {image_path} does not exist."
            )
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

                # The first SIGTERM will close the matplotlib window and
                # stop to display the predictions

                display_prediction = False
                plt.close()
                continue

            else:

                # The second SIGTERM will stop the program

                break

        print(f"Accuracy: {correct_predictions / total_predictions}\n")
