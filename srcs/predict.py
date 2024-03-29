from mlpackage.colors_variable import RED, GREEN, RESET
from mlpackage.parsers.predict import parse_arguments
from mlpackage.predict.load_model import load_model
from mlpackage.predict.predict_validation_set import predict_validation_set
from mlpackage.predict.predict_image import predict_image
from pyfiglet import Figlet


def intro():
    print(
        f"{GREEN}{Figlet(font='big').renderText('Predict')}{RESET}""" +
        "This program is used to make predictions on an image or",
        "the predictions of the validation set.\n"
    )


if __name__ == "__main__":

    try:

        intro()

        (
            image_path,
            model_path,
            list_transformations,
            is_predict_validation_set
        ) = parse_arguments()

        (
            model,
            class_names,
            validation_paths
        ) = load_model(model_path, is_predict_validation_set)

        if is_predict_validation_set:
            predict_validation_set(
                validation_paths,
                model,
                class_names,
                list_transformations
            )

        else:
            predict_image(
                image_path,
                model,
                class_names,
                list_transformations,
                display_prediction=True
            )

    except Exception as error:
        print(f"{RED}Error:{RESET} {error}")
        exit()

    exit()
