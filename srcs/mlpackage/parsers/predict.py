# import argparse


def parse_arguments():

    image_path = "./microdb/Apple/image (11).JPG"

    model_path = "model"

    list_transformations = [
        "Doublewithoutbg"
    ]

    is_predict_validation_set = False

    return (
        image_path,
        model_path,
        list_transformations,
        is_predict_validation_set
    )
