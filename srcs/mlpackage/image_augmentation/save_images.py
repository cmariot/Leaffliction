import cv2 as cv


GREEN = "\033[92m"
RESET = "\033[0m"


def parse_extension(filename: str) -> tuple:

    """
    The point_pos is the index of the last '.' in the filename
    It's used to get the position of the extension (.jpg)
    Two cases :
    - There is an extension -> extension = filename[point_pos:]
    - There is no extension -> extension = ""
    """

    point_pos = filename.rfind(".")
    if point_pos != -1:
        extension = filename[point_pos:]
        filename = filename[:point_pos]
    else:
        extension = ""
    return filename, extension


def save_images(images: dict, filename: str) -> None:

    """
    Save the augmented images with the label added to the original image name

    Args:
    - images: dictionary with the label of the image as key and the augmented
    image as value
    - filename: the path of the original image

    The function uses the parse_extension function to get the filename and the
    extension of the file

    The label is added to the image name, just before the extension, and the
    image is saved
    """

    filename, extension = parse_extension(filename)

    for label, image in images.items():
        if label != "Original":
            # Add the label to the image name, just before the extension, and
            # save the image
            image_name = filename + "_" + label + extension
            cv.imwrite(image_name, image)
            print(f"The image {GREEN}{image_name}{RESET} has been saved.")
