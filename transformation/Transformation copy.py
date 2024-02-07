# https://plantcv.readthedocs.io/en/v3.4.1/vis_tutorial/

import argparse
from plantcv import plantcv as pcv
import os
import matplotlib.pyplot as plt
from matplotlib import image as mplimg
import cv2
import time


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
        default='.',
        help='Destination of the transformed image',
    )

    # Blur
    parser.add_argument(
        '-blur',
        type=bool,
        default=True,
        help='Do not display/save the blur the image',
    )

    # Mask
    parser.add_argument(
        '-mask',
        type=bool,
        default=True,
        help='Do not display/save the mask of the transformed image',
    )

    # ROI
    parser.add_argument(
        '-roi',
        type=bool,
        default=True,
        help='Do not display/save the ROI of the transformed image',
    )

    # Object
    parser.add_argument(
        '-obj',
        type=bool,
        default=True,
        help='Do not display/save the object of the transformed image',
    )

    # Pseudolandmark
    parser.add_argument(
        '-pseudo',
        type=bool,
        default=True,
        help='Do not display/save the pseudolandmark of the transformed image',
    )

    args = parser.parse_args()

    options = [args.blur, args.mask, args.roi, args.obj, args.pseudo]

    return (
        args.path,
        args.dst,
        options
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
    pcv.analyze.color(rgb_img=image, colorspaces="all", labeled_mask=labels,label="default")

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



def display_transformations(image_path, dest, options, is_launch_on_dir=False):

    # pcv.params.debug = "plot"
    # pcv.params.debug = "print"

    # Open the image with plantcv and matplotlib
    # The color of the pcv image is changed :/
    image, _, _ = pcv.readimage(image_path, mode='rgb')
    # pcv.plot_image(image)


    # Test create a mask

    # # Convert the image to grayscale based on one of the color channels
    # l = pcv.rgb2gray_lab(rgb_img=image, channel='l')
    # b = pcv.rgb2gray_lab(rgb_img=image, channel='b')
    # # pcv.plot_image(l)
    # # pcv.plot_image(b)

    # # With the grayscale image, we can apply a threshold to create a binary image
    # # -> Get the best threshold value for the 'b' channel
    # # Apply the threshold to the grayscale image
    # value_threshold = determine_threshold(b)
    # b_thresh = pcv.threshold.binary(gray_img=b, threshold=value_threshold,object_type='light')
    # l_thresh = pcv.threshold.binary(gray_img=l, threshold=91, object_type='light')
    # # pcv.plot_image(b_thresh)
    # # pcv.plot_image(l_thresh)
    # # exit()

    # # Fusion of the 2 binary images in a mask
    # bl_mask = pcv.logical_and(bin_img1=b_thresh, bin_img2=l_thresh)
    # # pcv.plot_image(bl_mask)

    # # Remve small objects from the mask that are not part of the plant
    # mask = pcv.fill(bin_img=bl_mask, size=100)
    # # pcv.plot_image(mask)

    # # Blur the mask to reduce the noise in the mask
    # blured_mask = pcv.gaussian_blur(img=mask, ksize=(3, 3))
    # # pcv.plot_image(blured_mask)

    # # Apply the mask to the image to get the masked image
    # mask_applied = pcv.apply_mask(img=image, mask=blured_mask, mask_color='white')
    # # pcv.plot_image(mask_applied)
    # # exit()
    from rembg import remove

    image_with_bg = image.copy()
    image_without_bg = remove(image_with_bg)

    # pcv.plot_image(image_with_bg)
    # pcv.plot_image(image_without_bg)







    # pcv.plot_image(image_with_bg)
    # s = pcv.rgb2gray_hsv(rgb_img = wimage_without_bg, channel='s')
    b = pcv.rgb2gray_lab(rgb_img = image_without_bg, channel='l')
    b_thresh = pcv.threshold.binary(gray_img=b, threshold=35, object_type='light')
    # for thres in range(0, 255, 10):
    #     b_thresh = pcv.threshold.binary(gray_img=b, threshold=thres, object_type='light')
    #     print("b_thresh", thres)
    #     pcv.plot_image(b_thresh)

    # print("b_thresh")
    # pcv.plot_image(b_thresh)
    filled = pcv.fill(bin_img=b_thresh, size=200)
    # print("filled")
    # pcv.plot_image(filled)
    gaussian_bluri = pcv.gaussian_blur(img=filled, ksize=(3, 3))
    # print("gaussian blur")
    # pcv.plot_image(gaussian_bluri)
    masked = pcv.apply_mask(img=image_with_bg, mask=gaussian_bluri, mask_color='black')




    # pcv.plot_image(b_thresh)
    # pcv.plot_image(gaussian_bluri)
    # pcv.plot_image(filled)
    # pcv.plot_image(masked)


    # pcv.plot_image(gaussian_blurf(s_thresh, 80))

    # l = pcv.rgb2gray_lab(rgb_img=image, channel='l')
    # #pcv.plot_image(l)
    # l_thresh = pcv.threshold.binary(gray_img=l, threshold=30, object_type='light')
    # #pcv.plot_image(l_thresh)

    # b = pcv.rgb2gray_lab(rgb_img=image, channel='b')
    # #pcv.plot_image(b)
    # value_threshold = determine_threshold(b)
    # b_thresh=pcv.threshold.binary(gray_img=b, threshold=value_threshold,object_type='light')
    # #print("Value treshold:", value_threshold)
    # #pcv.plot_image(b_thresh)

    # bminusl_thresh = pcv.apply_mask(img=b_thresh, mask=l_thresh, mask_color='black')

    # masked = pcv.apply_mask(img=image, mask=bminusl_thresh, mask_color='white')
    # gaussian_bluri = gaussian_blurf(masked, 80)


    # pcv.plot_image(gaussian_bluri)
    # print("gaussian blur")

    # b_fill = pcv.fill(bin_img=bminusl_thresh, size=200)

    # masked2= pcv.apply_mask(img=masked, mask=b_fill, mask_color='white')
    # pcv.plot_image(masked2)





    # bminusl_thresh = pcv.apply_mask(img=b_thresh, mask=l_thresh, mask_color='black')

    # # The blur is used to reduce the noise in the mask
    # gaussian_bluri = pcv.gaussian_blur(img=bminusl_thresh, ksize=(5, 5), sigma_x=0, sigma_y=None)

    # # Apply the mask to the image to get the masked image
    # masked = pcv.apply_mask(img=image, mask=gaussian_bluri, mask_color='white')
    # b_fill = pcv.fill(bin_img=bminusl_thresh, size=200)
    # masked2 = pcv.apply_mask(img=masked, mask=b_fill, mask_color='white')

    # pcv.plot_image(bminusl_thresh)
    # pcv.plot_image(b_fill)
    # pcv.plot_image(masked2)

    # pcv.plot_image(masked2)


    # id_objects, obj_hierarchy = pcv.find_objects(masked2, b_fill)

    # roi, roi_hierarchy= pcv.roi.rectangle(img=masked2, x=0, y=0, w=image.shape[0], h=image.shape[1])

    # roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=image, roi_contour=roi,
    #                                                                 roi_hierarchy=roi_hierarchy,
    #                                                                 object_contour=id_objects,
    #                                                                 obj_hierarchy=obj_hierarchy,
    #                                                                 roi_type='partial')

    # obj, mask = pcv.object_composition(img=image, contours=roi_objects, hierarchy=hierarchy3)

    # # pcv.plot_image(mask)

    # shape_img = pcv.analyze_object(img=image, obj=obj, mask=mask, label="default")
    # # pcv.plot_image(shape_img)
    # boundary_img1 = pcv.analyze_bound_horizontal(img=image, obj=obj, mask=mask,
    #                                                line_position=1680, label="default")

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

    pcv.analyze.color(rgb_img=image, colorspaces="all", labeled_mask=kept_mask,label="default")

    fig, ax = plt.subplots(ncols=3, nrows=2, figsize=(16, 9))

    fig.suptitle(f"Transformation of {image_path}")

    images_to_plot = {
        "Original": cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
        "Gaussian blur": cv2.cvtColor(gaussian_bluri, cv2.COLOR_BGR2RGB),
        "Mask": cv2.cvtColor(masked, cv2.COLOR_BGR2RGB),
        "ROI Objects": cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB),
        "Analyze object": cv2.cvtColor(analysis_image, cv2.COLOR_BGR2RGB),
        "Pseudolandmarks": cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    }

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
        plt.show()
        # plt.show(block=False)
        # plt.pause(.5)
        # plt.close()
    else:
        plt.show()
        plot_histogram(image, kept_mask)


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
    for image in images_list:
        display_transformations(image, dest, options, is_launch_on_dir=True)


def main():

    path, dest, options = parse_argument()

    if os.path.isfile(path):
        display_transformations(path, dest, options)
    elif os.path.isdir(path):
        transform_directory(path, dest, options)
    else:
        raise Exception("The path is not a file or a directory")


if __name__ == "__main__":
    # main()
    try:
        main()
    except KeyboardInterrupt:
        print("\nSIGTERM")
        exit()
    except Exception as error:
        print(error)
        exit(1)