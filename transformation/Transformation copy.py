# https://plantcv.readthedocs.io/en/v3.4.1/vis_tutorial/

import argparse
from plantcv import plantcv as pcv
import os
import matplotlib.pyplot as plt
import cv2
from rembg import remove
from tqdm import tqdm
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
        If the path is a directory, display the transformation of all the images
        in the directory and save them in the 'dest' directory.
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


def total_luminosity(image):
    tot = 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            tot = tot + image[i][j]
    return tot


def roughlyinferior(a, b):
    if a  < b + 10 / 100 * b:
        return True
    return False

def determine_threshold(b):
    b_thresh = pcv.threshold.binary(
        gray_img=b,
        threshold=50,
        object_type='light'
    )
    past_lum = total_luminosity(b_thresh)
    max_diff = 0
    iter = 0
    for loop in range(50, 250, 5):
        b_thresh = pcv.threshold.binary(
            gray_img=b, threshold=loop, object_type='light'
        )
        #pcv.plot_image(b_thresh)
        cur_lum = total_luminosity(b_thresh)
        diff = past_lum - cur_lum

        if max_diff < diff:
            max_diff = diff
        print("iter", loop, "lum", cur_lum, "delta", diff)
        if (max_diff != diff):
            iter = loop
            #print("this one")
            return iter

        past_lum = cur_lum
    max_diff = diff

    for loop in range(iter, 250, 1):
        b_thresh = pcv.threshold.binary(
            gray_img=b, threshold=loop, object_type='light'
        )
        cur_lum = total_luminosity(b_thresh)
        diff = past_lum - cur_lum
        # print("iter", loop, "lum", cur_lum, "delta", diff)
        if max_diff > diff:
            max_diff = diff
        if (max_diff != diff):
            # print("this one")
            return loop
        past_lum = cur_lum
    return 0


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

    # Draw the top line
    if (
        (x >= roi_start_x and x <= roi_start_x + roi_w)
            and
        (y >= roi_start_y and y <= roi_start_y + roi_line_w)
    ):
        return True

    # Draw the bottom line
    if (
        (x >= roi_start_x and x <= roi_start_x + roi_w)
            and
        (y >= roi_start_y + roi_h - roi_line_w and y <= roi_start_y + roi_h)
    ):
        return True

    # Draw the left line
    if (
        (x >= roi_start_x and x <= roi_start_x + roi_line_w)
            and
        (y >= roi_start_y and y <= roi_start_y + roi_h)
    ):
        return True

    # Draw the right line
    if (
        (x >= roi_start_x + roi_w - roi_line_w and x <= roi_start_x + roi_w)
            and
        (y >= roi_start_y and y <= roi_start_y + roi_h)
    ):
        return True

    return False


def plot_histogram(image, kept_mask):

    def plot_stat_hist(label, sc=1):
        y = pcv.outputs.observations['default_1'][label]['value']
        x = [i * sc for i in  pcv.outputs.observations['default_1'][label]['label']]
        if label == "hue_frequencies":
            x = x[:int(255 / 2)]
            y = y[:int(255 / 2)]
        if label == "blue-yellow_frequencies" or label == "green-magenta_frequencies":
            x = [x + 128 for x in x]
        plt.plot(x, y, label=label)
        return


    labels, obj = pcv.create_labels(mask=kept_mask)
    pcv.analyze.color(rgb_img=image, colorspaces="all", labeled_mask=labels, label="default")

    plt.subplots(figsize=(16, 9))

    dict_label = {
        "blue_frequencies" : 1,
        "green_frequencies": 1,
        "green-magenta_frequencies" : 1 ,
        "lightness_frequencies" : 2.55,
        "red_frequencies" : 1,
        "blue-yellow_frequencies" : 1,
        "hue_frequencies" : 1,
        "saturation_frequencies" : 2.55,
        "value_frequencies" : 2.55
    }

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


def gaussian_blurf(img, sat):
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=sat, object_type='light')
    gaussian_bluri = pcv.gaussian_blur(img=s_thresh, ksize=(5, 5), sigma_x=0, sigma_y=None)
    return gaussian_bluri



def display_transformations(image_path, dest, options, is_launch_on_dir=False, dir_name=""):

    # pcv.params.debug = "plot"
    # pcv.params.debug = "print"

    # Open the image with plantcv and matplotlib
    # The color of the pcv image is changed :/
    image, _, _ = pcv.readimage(image_path, mode='rgb')


    image_with_bg = image.copy()
    image_without_bg = remove(image_with_bg)

    b = pcv.rgb2gray_lab(rgb_img = image_without_bg, channel='l')
    b_thresh = pcv.threshold.binary(gray_img=b, threshold=35, object_type='light')

    filled = pcv.fill(bin_img=b_thresh, size=200)

    gaussian_bluri = pcv.gaussian_blur(img=filled, ksize=(3, 3))

    masked = pcv.apply_mask(img=image_with_bg, mask=gaussian_bluri, mask_color='black')

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

    kept_mask = pcv.roi.filter(mask=filled, roi=roi, roi_type='partial')

    roi_image = image.copy()
    roi_image[kept_mask != 0] = (0, 255, 0)
    for x in range(0, image.shape[0]):
        for y in range(0, image.shape[1]):
            if is_roi_border(x, y, roi_start_x, roi_start_y, roi_h, roi_w, roi_line_w):
                roi_image[x, y] = (255, 0, 0)

    analysis_image = pcv.analyze.size(img=image, labeled_mask=kept_mask)

    images_to_plot = {
        "Original": cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
        "Gaussian blur": cv2.cvtColor(gaussian_bluri, cv2.COLOR_BGR2RGB),
        "Mask": cv2.cvtColor(masked, cv2.COLOR_BGR2RGB),
        "ROI Objects": cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB),
        "Analyze object": cv2.cvtColor(analysis_image, cv2.COLOR_BGR2RGB),
        "Pseudolandmarks": cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    }

    fig, ax = plt.subplots(ncols=3, nrows=2, figsize=(16, 9))

    fig.suptitle(f"Transformation of {image_path}")

    for (label, img), axe in zip(images_to_plot.items(), ax.flat):
        axe.imshow(img)
        axe.set_title(label)
        axe.set(xticks=[], yticks=[])
        axe.label_outer()

    top_x, bottom_x, center_v_x = pcv.homology.x_axis_pseudolandmarks(img=image, mask=filled, label='default')

    for i in range(len(top_x)):
        if len(top_x[i]) >= 1 and len(top_x[i][0]) >= 2:
            plt.scatter(top_x[i][0][0], top_x[i][0][1], c='blue', s=10)
    for i in range(len(bottom_x)):
        if len(bottom_x[i]) >= 1 and len(bottom_x[i][0]) >= 2:
            plt.scatter(bottom_x[i][0][0], bottom_x[i][0][1], c='magenta', s=10)
    for i in range(len(center_v_x)):
        if len(center_v_x[i]) >= 1 and len(center_v_x[i][0]) >= 2:
            plt.scatter(center_v_x[i][0][0], center_v_x[i][0][1], c='orange', s=10)

    if is_launch_on_dir:

        new_image_path = image_path.replace(dir_name, dest, 1)

        dirs = new_image_path.split("/")

        for i in range(len(dirs) - 1):
            dir_to_create = "/".join(dirs[:i + 1])
            if not os.path.isdir(dir_to_create):
                os.mkdir(dir_to_create)

        point_pos = image_path.rfind(".")

        if point_pos == -1:
            filename_without_ext = image_path.replace(dir_name, dest, 1)
            extension = ""
        else:
            filename_without_ext = image_path[:point_pos].replace(dir_name, dest, 1)
            extension = image_path[point_pos:]

        for label, img in images_to_plot.items():
            if label in options:
                image_name = f"{filename_without_ext}_{label}{extension}"
                cv2.imwrite(image_name, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                print(f"Image saved at {image_name}")

    else:
        plt.show()
        plot_histogram(image, kept_mask)

    plt.close()


def get_image_list(path: str) -> list:

    """
    Return the llist of files in the directory associated with 'path'
    It walks in the subdirectories
    """

    image_list = []
    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            image_list.append(full_path)
    return image_list


def transform_directory(path, dest, options):
    images_list: list = get_image_list(path)
    for image in tqdm(images_list):
        display_transformations(image, dest, options, is_launch_on_dir=True, dir_name=path)


def main():

    path, dest, options = parse_argument()

    if os.path.isfile(path):
        display_transformations(path, dest, options)
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
