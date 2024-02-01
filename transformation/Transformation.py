# Open original file w/ plantcv

# Links :
# - Gaussian blur :
# - Mask :
# - ROI Objects :
# - Analyse Objects :     https://plantcv.readthedocs.io/en/stable/tutorials/morphology_tutorial/
# - Pseudolandmarks :

# Display a color histogram

import argparse
from plantcv import plantcv as pcv


def parse_argument() -> str:

    """
    Parse the argument of the program,
    return the path of the image to transform
    """
    parser = argparse.ArgumentParser(
        prog='Transformation',
        description="Transform an image",
    )
    parser.add_argument('image_path')
    args = parser.parse_args()
    return args.image_path


def gaussian_blur(image):
    grayscale_img = pcv.rgb2gray_cmyk(
        rgb_img=image,
        channel='C'
    )
    # inverted = pcv.invert(grayscale_img)
    gaussian_img = pcv.gaussian_blur(
        img=grayscale_img,
        ksize=(11, 11),
        sigma_x=0,
        sigma_y=None
    )
    return gaussian_img


def main():
    image_path = parse_argument()
    image, path, name = pcv.readimage(image_path)
    pcv.plot_image(image)

    transformations = {
        "Gaussian Blur": gaussian_blur,
    }

    for key, value in transformations.items():
        print(key)
        transformed_image = value(image)
        pcv.plot_image(transformed_image)



if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
        exit(1)