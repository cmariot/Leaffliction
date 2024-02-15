import argparse
from plantcv import plantcv as pcv
import os
import matplotlib.pyplot as plt
import cv2
import rembg
import numpy as np
from tqdm import tqdm


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
        help='Path of the image / direcrory of image to transform',
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


def is_roi_border(x, y, roi_start_x, roi_start_y, roi_h, roi_w, roi_line_w):
    """
    Return true if the pixel in position x, y is the border of the rectangle
    defined by the roi parameters.
    The contour is the line of the rectangle, with a width of roi_line_w.

    :param x: The x position of the pixel
    :param y: The y position of the pixel
    :param roi_start_x: The x position of the roi rectangle start
    :param roi_start_y: The y position of the roi rectangle start
    :param roi_h: The height of the roi rectangle
    :param roi_w: The width of the roi rectangle
    :param roi_line_w: The width of the roi rectangle line
    """

    return (
        (
            roi_start_x <= x <= roi_start_x + roi_w and
            roi_start_y <= y <= roi_start_y + roi_line_w
        )
        or
        (
            roi_start_x <= x <= roi_start_x + roi_w and
            roi_start_y + roi_h - roi_line_w <= y <= roi_start_y + roi_h
        )
        or
        (
            roi_start_x <= x <= roi_start_x + roi_line_w and
            roi_start_y <= y <= roi_start_y + roi_h
        )
        or
        (
            roi_start_x + roi_w - roi_line_w <= x <= roi_start_x + roi_w and
            roi_start_y <= y <= roi_start_y + roi_h
        )
    )


def create_roi_image(
    image,
    masked,
    filled
):

    """
    Create an image with the ROI rectangle and the mask
    """

    # Create a region of interest (ROI) rectangle
    roi_start_x = 0
    roi_start_y = 0
    roi_w = image.shape[0]
    roi_h = image.shape[1]
    roi_line_w = 5

    roi = pcv.roi.rectangle(
        img=masked,
        x=roi_start_x,
        y=roi_start_y,
        w=roi_w,
        h=roi_h
    )

    # Create a mask based on the ROI
    kept_mask = pcv.roi.filter(mask=filled, roi=roi, roi_type='partial')

    roi_image = image.copy()
    roi_image[kept_mask != 0] = (0, 255, 0)
    for x in range(0, image.shape[0]):
        for y in range(0, image.shape[1]):
            if is_roi_border(x, y, roi_start_x, roi_start_y,
                             roi_h, roi_w, roi_line_w):
                roi_image[x, y] = (255, 0, 0)

    return roi_image, kept_mask


def plot_histogram(image, kept_mask):

    """
    Plot the histogram of the image
    """

    def plot_stat_hist(label, sc=1):

        """
        Retrieve the histogram x and y values and plot them
        """

        y = pcv.outputs.observations['default_1'][label]['value']
        x = [
            i * sc
            for i in pcv.outputs.observations['default_1'][label]['label']
        ]
        if label == "hue_frequencies":
            x = x[:int(255 / 2)]
            y = y[:int(255 / 2)]
        if (
            label == "blue-yellow_frequencies" or
            label == "green-magenta_frequencies"
        ):
            x = [x + 128 for x in x]
        plt.plot(x, y, label=label)
        return

    dict_label = {
        "blue_frequencies": 1,
        "green_frequencies": 1,
        "green-magenta_frequencies": 1,
        "lightness_frequencies": 2.55,
        "red_frequencies": 1,
        "blue-yellow_frequencies": 1,
        "hue_frequencies": 1,
        "saturation_frequencies": 2.55,
        "value_frequencies": 2.55
    }

    labels, _ = pcv.create_labels(mask=kept_mask)
    pcv.analyze.color(
        rgb_img=image,
        colorspaces="all",
        labeled_mask=labels,
        label="default"
    )

    plt.subplots(figsize=(16, 9))
    for key, val in dict_label.items():
        plot_stat_hist(key, val)

    plt.legend()

    plt.title("Color Histogram")
    plt.xlabel("Pixel intensity")
    plt.ylabel("Proportion of pixels (%)")
    plt.grid(
        visible=True,
        which='major',
        axis='both',
        linestyle='--',
    )
    plt.show()
    plt.close()


def is_in_circle(x, y, center_x, center_y, radius):
    """
    Return True if the pixel (x, y) is in the circle defined by center_x,
    center_y and radius
    """

    if (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2:
        return True
    return False


def draw_pseudolandmarks(image, pseudolandmarks, color, radius):

    """
    Draw a circle in the image,
    Replace the pixels of 'image' by the color by a circle centered on
    """

    for i in range(len(pseudolandmarks)):
        if len(pseudolandmarks[i]) >= 1 and len(pseudolandmarks[i][0]) >= 2:
            center_x = pseudolandmarks[i][0][1]
            center_y = pseudolandmarks[i][0][0]
            for x in range(image.shape[0]):
                for y in range(image.shape[1]):
                    if is_in_circle(x, y, center_x, center_y, radius):
                        image[x, y] = color
    return image


def create_pseudolandmarks_image(image, kept_mask):
    """
    Create a displayable image with the pseudolandmarks
    """
    pseudolandmarks = image.copy()
    top_x, bottom_x, center_v_x = pcv.homology.x_axis_pseudolandmarks(
        img=pseudolandmarks, mask=kept_mask, label='default'
    )
    pseudolandmarks = draw_pseudolandmarks(
        pseudolandmarks, top_x, (0, 0, 255), 5
    )
    pseudolandmarks = draw_pseudolandmarks(
        pseudolandmarks, bottom_x, (255, 0, 255), 5
    )
    pseudolandmarks = draw_pseudolandmarks(
        pseudolandmarks, center_v_x, (255, 0, 0), 5
    )
    return pseudolandmarks


def get_image_name(new_path, label):

    """
    Return the name of the image to save
    """

    point_index = new_path.rfind(".")
    label = label.replace(" ", "_")
    if point_index == -1:
        return new_path + "_" + label
    else:
        return new_path[:point_index] + "_" + label + new_path[point_index:]


def transform_image(
    image_path,
    options,
    is_launch_on_dir=False,
    new_path=""
):

    # Open the image with plantcv
    image, _, _ = pcv.readimage(image_path, mode='rgb')

    # Remove the background of the image
    image_without_bg = rembg.remove(image)

    # Convert the image to grayscale
    l_grayscale = pcv.rgb2gray_lab(rgb_img=image_without_bg, channel='l')

    # Create a binary image with a threshold
    l_thresh = pcv.threshold.binary(
        gray_img=l_grayscale, threshold=35, object_type='light'
    )

    # Remove small objects from the binary image that are smaller than 200 pxls
    filled = pcv.fill(bin_img=l_thresh, size=200)

    # Apply a gaussian blur to the image to remove the noise
    gaussian_bluri = pcv.gaussian_blur(img=filled, ksize=(3, 3))

    # Apply a mask to the image
    masked = pcv.apply_mask(img=image, mask=gaussian_bluri, mask_color='black')

    # Create a displayable image with the ROI rectangle and the mask
    roi_image, kept_mask = create_roi_image(
        image, masked, filled
    )

    # Analyze the object in the image
    analysis_image = pcv.analyze.size(img=image, labeled_mask=kept_mask)

    # Create a displayable image with the pseudolandmarks
    pseudolandmarks = create_pseudolandmarks_image(
        image, kept_mask
    )

    images = {
        "Original": cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
        "Gaussian blur": cv2.cvtColor(gaussian_bluri, cv2.COLOR_BGR2RGB),
        "Mask": cv2.cvtColor(masked, cv2.COLOR_BGR2RGB),
        "ROI Objects": cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB),
        "Analyze object": cv2.cvtColor(analysis_image, cv2.COLOR_BGR2RGB),
        "Pseudolandmarks": cv2.cvtColor(pseudolandmarks, cv2.COLOR_BGR2RGB)
    }

    # Used in predict.py to return the transformed images
    if is_launch_on_dir is None:
        [images.pop(key) for key in images.keys() - options]
        return images

    # If the argument of the program is a file, display the transformation
    if not is_launch_on_dir:

        # Create the figure to plot
        fig, ax = plt.subplots(ncols=3, nrows=2, figsize=(16, 9))

        # Title of the plot
        fig.suptitle(f"Transformation of {image_path}")

        # Put the images on the plot
        for (label, img), axe in zip(images.items(), ax.flat):
            axe.imshow(img)
            axe.set_title(label)
            axe.set(xticks=[], yticks=[])
            axe.label_outer()

        plt.show()
        plt.close()

        plot_histogram(image, kept_mask)

    # Else if the argument of the program is a directory,
    # save the transformations
    elif is_launch_on_dir:

        for label, img in images.items():
            if label in options:
                cv2.imwrite(
                    get_image_name(new_path, label),
                    cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                )


def transform_directory(path, dest, options):

    """
    Transform all the images in the directory 'path' and save them in the
    'dest' directory
    """

    if not os.path.isdir(dest):

        os.makedirs(dest)
        # split_path = dest.split("/")

        # for i in range(1, len(split_path) + 1):
        #     new_path = "/".join(split_path[:i])
        #     print(f"Test to create {new_path}")
        #     if not os.path.isdir(new_path):
        #         print(f"Create directory {new_path}")
        #         os.mkdir(new_path)

    for root, dirs, files in os.walk(path):

        new_root = root.replace(path, dest, 1)

        for dir in dirs:
            if not os.path.isdir(os.path.join(new_root, dir)):
                os.mkdir(os.path.join(new_root, dir))

        for file in tqdm(files):
            full_path = os.path.join(root, file)
            new_path = os.path.join(new_root, file)
            transform_image(
                full_path,
                options,
                is_launch_on_dir=True,
                new_path=new_path
            )


def main():

    """
    Main function of the program,
    it calls the other functions depending on the path
    - If the path is a file, display the transformation of the image.
    - If the path is a directory, save the transformation of all the images
    """

    path, dest, options = parse_argument()

    if os.path.isfile(path):
        transform_image(path, options)
    elif os.path.isdir(path):
        transform_directory(path, dest, options)
    else:
        raise Exception("The path is not a file or a directory")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSIGTERM")
        exit()
    except Exception as error:
        print(error)
        exit(1)
