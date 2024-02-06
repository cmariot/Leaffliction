# https://plantcv.readthedocs.io/en/v3.4.1/vis_tutorial/

import argparse
from plantcv import plantcv as pcv
import os
import matplotlib.pyplot as plt
from matplotlib import image as mplimg


def parse_argument() -> str:

    """
    Parse the argument of the program,
    return the path of the image to transform
    """

    parser = argparse.ArgumentParser(
        prog='Transformation.py',
        description="""
        If the path is a file, display the transformation of the image.
        If the path is a directory, display the transformation of all the images in the directory and save them in the 'dest' directory.
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



def determine_threshold(b):
    b_thresh=pcv.threshold.binary(gray_img=b, threshold=50,object_type='light')
    past_lum = total_luminosity(b_thresh)
    max_diff = 0
    iter = 0
    for loop in range(50, 250, 2):
        b_thresh=pcv.threshold.binary(gray_img=b, threshold=loop,object_type='light')
        #pcv.plot_image(b_thresh)
        cur_lum = total_luminosity(b_thresh)
        diff = past_lum - cur_lum

        if max_diff < diff:
            max_diff = diff
        #print("iter", loop, "lum", cur_lum, "delta", diff)
        if (max_diff != diff):
            iter = loop
            break
        past_lum = cur_lum
    max_diff = diff

    for loop in range(iter, 250, 1):
        b_thresh=pcv.threshold.binary(gray_img=b, threshold=loop, object_type='light')
        cur_lum = total_luminosity(b_thresh)
        diff = past_lum - cur_lum
        #print("iter", loop, "lum", cur_lum, "delta", diff)
        if max_diff > diff:
            max_diff = diff
        if (max_diff != diff):
            #print("this one")
            return loop
        past_lum = cur_lum
    return 0

def gaussian_blurf(img, sat):
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=sat, object_type='light')
    gaussian_bluri = pcv.gaussian_blur(img=s_thresh, ksize=(5, 5), sigma_x=0, sigma_y=None)
    return gaussian_bluri


def plot_histogram():

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
    plt.show()


def display_transformations(image_path, dest, options):

    # pcv.params.debug = "plot"
    # pcv.params.debug = "print"

    # Open the image with plantcv and matplotlib
    # The color of the pcv image is changed :/
    image, _, _ = pcv.readimage(image_path, mode='rgb')
    original_image = mplimg.imread(image_path)
    pcv.plot_image(image)

    # Convert the image to grayscale based on one of the color channels
    l = pcv.rgb2gray_lab(rgb_img=image, channel='l')
    b = pcv.rgb2gray_lab(rgb_img=image, channel='b')
    # pcv.plot_image(l)
    # pcv.plot_image(b)

    # With the grayscale image, we can apply a threshold to create a binary image
    # -> Get the best threshold value for the 'b' channel
    # Apply the threshold to the grayscale image
    value_threshold = determine_threshold(b)
    b_thresh = pcv.threshold.binary(gray_img=b, threshold=value_threshold,object_type='light')
    l_thresh = pcv.threshold.binary(gray_img=l, threshold=30, object_type='light')
    # pcv.plot_image(b_thresh)
    # pcv.plot_image(l_thresh)

    # Fusion of the 2 binary images in a mask
    bminusl_thresh = pcv.apply_mask(img=b_thresh, mask=l_thresh, mask_color='black')
    # pcv.plot_image(bminusl_thresh)

    # Apply the mask to the image to get the masked image
    masked = pcv.apply_mask(img=image, mask=bminusl_thresh, mask_color='white')
    # pcv.plot_image(masked)

    # The blur is used to reduce the noise in the mask
    gaussian_bluri = gaussian_blurf(masked, 80)
    pcv.plot_image(gaussian_bluri)
    exit()

    b_fill = pcv.fill(bin_img=bminusl_thresh, size=200)

    masked2= pcv.apply_mask(img=masked, mask=b_fill, mask_color='white')

    gaussian_bluri = gaussian_blurf(masked2, 80)

    pcv.plot_image(gaussian_bluri)

    pcv.plot_image(masked2)

    roi = pcv.roi.rectangle(img=masked2, x=0, y=0, w=image.shape[0], h=image.shape[1])
    kept_mask = pcv.roi.filter(mask=b_fill, roi=roi, roi_type='partial')

    labelo, obj = pcv.create_labels(mask=kept_mask)

    pcv.plot_image(labelo)

    analysis_image = pcv.analyze.size(img=image, labeled_mask=kept_mask)

    pcv.plot_image(analysis_image)

    pcv.analyze.color(rgb_img=image, colorspaces="all", labeled_mask=kept_mask,label="default")

    # _, ax = plt.subplots(ncols=3, nrows=2, figsize=(16, 9))

    # images_to_plot = {
    #     "Original": original_image,
    #     "Gaussian blur": blur,
    #     "Mask": masked,
    #     "ROI Objects": labelo,
    #     "Analyze object":analysis_image,
    #     "Pseudolandmarks": original_image
    # }

    # for (label, img), axe in zip(images_to_plot.items(), ax.flat):
    #     axe.imshow(img)
    #     axe.set_title(label)
    #     axe.set(xticks=[], yticks=[])
    #     axe.label_outer()

    plt.imshow(original_image)
    top_x, bottom_x, center_v_x = pcv.homology.x_axis_pseudolandmarks(img=image, mask=b_fill, label='default')

    for i in range(len(top_x)):
        plt.scatter(top_x[i][0][0], top_x[i][0][1], c='blue', s=10)
    for i in range(len(bottom_x)):
        plt.scatter(bottom_x[i][0][0], bottom_x[i][0][1], c='magenta', s=10)
    for i in range(len(center_v_x)):
        plt.scatter(center_v_x[i][0][0], center_v_x[i][0][1], c='orange', s=10)

    plt.show()

    # plot_histogram()




def main():

    path, dest, options = parse_argument()

    if os.path.isfile(path):
        display_transformations(path, dest, options)
    elif os.path.isdir(path):
        # transform_directory(path, dest, options)
        pass
    else:
        raise Exception("The path is not a file or a directory")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit()
    except Exception as error:
        print(error)
        exit(1)