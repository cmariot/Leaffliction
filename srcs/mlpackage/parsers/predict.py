import argparse


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--image_path",
        type=str,
        default=None,
        help="Path to the image to predict on. " +
             "If not provided, the model will predict on the validation set."
    )

    parser.add_argument(
        "--model_path",
        type=str,
        default="model",
        help="Path to the model"
    )

    args = parser.parse_args()

    image_path = args.image_path
    model_path = args.model_path
    is_predict_validation_set = True if args.image_path is None else False

    return (
        image_path,
        model_path,
        ["Doublewithoutbg"],
        is_predict_validation_set
    )
