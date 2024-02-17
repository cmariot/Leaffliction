import argparse
import numpy as np


def parse_argument() -> str:

    """
    Parse the argument of the program,
    return the path of the image to transform
    """

    parser = argparse.ArgumentParser(
        prog='Transformation.py',
        description="""
        If the path is a file, display the transformation of the image.
        If the path is a directory, display the transformation of all the
        images in the directory and save them in the 'dest' directory.
        """
    )

    parser.add_argument(
        dest='path',
        type=str,
        help='Path of the image / directory of image to transform',
    )

    parser.add_argument(
        '-dst',
        type=str,
        default='../transformed_directory',
        help='Destination of the transformed image',
    )

    # Blur
    parser.add_argument(
        '-blur', '-b',
        default=False,
        action='store_true',
        help='Do not display/save the blur the image',
    )

    # Mask
    parser.add_argument(
        '-mask', '-m',
        default=False,
        action='store_true',
        help='Do not display/save the mask of the transformed image',
    )

    # ROI
    parser.add_argument(
        '-roi', '-r',
        default=False,
        action='store_true',
        help='Do not display/save the ROI of the transformed image',
    )

    # Object
    parser.add_argument(
        '-obj', '-o',
        default=False,
        action='store_true',
        help='Do not display/save the object of the transformed image',
    )

    # Pseudolandmark
    parser.add_argument(
        '-pseudo', '-p',
        default=False,
        action='store_true',
        help='Do not display/save the pseudolandmark of the transformed image',
    )

    args = parser.parse_args()

    options = np.array([
        args.blur,
        args.mask,
        args.roi,
        args.obj,
        args.pseudo
    ])

    image_to_plot = np.array([
        "Gaussian blur",
        "Mask",
        "ROI Objects",
        "Analyze object",
        "Pseudolandmarks"
    ])

    return (
        args.path,
        args.dst,
        image_to_plot[options] if options.any() else image_to_plot
    )
