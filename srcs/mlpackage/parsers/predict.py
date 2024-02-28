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
        default="./model",
        help="Path to the model"
    )

    parser.add_argument(
        "--list_transformations",
        nargs="+",
        default=["Doublewithoutbg"],
        help="List of transformations"
    )

    args = parser.parse_args()

    is_predict_validation_set = True if args.image_path is None else False

    return (
        args.image_path,
        args.model_path,
        args.list_transformations,
        is_predict_validation_set
    )
