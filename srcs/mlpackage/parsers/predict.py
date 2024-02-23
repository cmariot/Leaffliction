# import argparse


def parse_arguments():

    image_path = "image.jpg"

    model_path = "model"

    list_transformations = [
        "Doublewithoutbg"
    ]

    is_predict_validation_set = True

    return (
        image_path,
        model_path,
        list_transformations,
        is_predict_validation_set
    )
