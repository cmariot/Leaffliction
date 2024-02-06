# https://plantcv.readthedocs.io/en/v3.4.1/vis_tutorial/

import argparse
from plantcv import plantcv as pcv
import os
import matplotlib.pyplot as plt
import cv2


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

def plot_stat_hist(label, sc=1):

    y = pcv.outputs.observations['default_1'][label]['value']
    x = [i * sc for i in  pcv.outputs.observations['default_1'][label]['label']]

    if label == "hue_frequencies":
        x = x[:int(255 / 2)]
        y = y[:int(255 / 2)]
    if label == "blue-yellow_frequencies" or label == "green-magenta_frequencies":
        x = [x + 128 for x in x]

    plt.plot(x, y, label=label)

def determine_threshold(b):
    b_thresh=pcv.threshold.binary(gray_img=b, threshold=50, max_value=255, object_type='light')
    past_lum = total_luminosity(b_thresh)
    max_diff = 0
    iter = 0
    for loop in range(50, 250, 2):
        b_thresh=pcv.threshold.binary(gray_img=b, threshold=loop, max_value=255, object_type='light')
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
        b_thresh=pcv.threshold.binary(gray_img=b, threshold=loop, max_value=255, object_type='light')
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
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=sat, max_value=255, object_type='light')
    gaussian_bluri = pcv.gaussian_blur(img=s_thresh, ksize=(5, 5), sigma_x=0, sigma_y=None)
    return gaussian_bluri

def plot_histogram(image, labeled_mask):

    pcv.analyze.color(rgb_img=image, colorspaces="all", labeled_mask=labeled_mask,label="default")

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

    print("plot histogram")
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

def display_transformations(image_path, dest, options):

    #pcv.params.debug = "print"

    image, path, name = pcv.readimage(image_path)
    #pcv.plot_image(image)
    #print("original")

    l = pcv.rgb2gray_lab(rgb_img=image, channel='l')
    #pcv.plot_image(l)
    l_thresh = pcv.threshold.binary(gray_img=l, threshold=30, max_value=255, object_type='light')
    #pcv.plot_image(l_thresh)

    b = pcv.rgb2gray_lab(rgb_img=image, channel='b')
    #pcv.plot_image(b)
    value_threshold = determine_threshold(b)
    print("Value b threshold", determine_threshold(b))
    # pcv.plot_image(pcv.threshold.binary(gray_img=b, threshold=116,object_type='light'))
    b_thresh=pcv.threshold.binary(gray_img=b, threshold=value_threshold,max_value=255, object_type='light')

    bminusl_thresh = pcv.apply_mask(img=b_thresh, mask=l_thresh, mask_color='black')

    masked = pcv.apply_mask(img=image, mask=bminusl_thresh, mask_color='white')
    gaussian_bluri = gaussian_blurf(masked, 80)

    #pcv.plot_image(gaussian_bluri)
    #print("gaussian blur")

    b_fill = pcv.fill(bin_img=bminusl_thresh, size=200)
    print("fill")

    masked2= pcv.apply_mask(img=masked, mask=b_fill, mask_color='white')
    print("mask")
    #pcv.plot_image(masked2)

    id_objects, obj_hierarchy = pcv.find_objects(masked2, b_fill)

    roi, roi_hierarchy= pcv.roi.rectangle(img=masked2, x=0, y=0, w=image.shape[0], h=image.shape[1])

    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=image, roi_contour=roi,
                                                                    roi_hierarchy=roi_hierarchy,
                                                                    object_contour=id_objects,
                                                                    obj_hierarchy=obj_hierarchy,
                                                                    roi_type='partial')

    obj, mask = pcv.object_composition(img=image, contours=roi_objects, hierarchy=hierarchy3)

    # pcv.plot_image(mask)

    shape_img = pcv.analyze_object(img=image, obj=obj, mask=mask, label="default")
    # pcv.plot_image(shape_img)
    boundary_img1 = pcv.analyze_bound_horizontal(img=image, obj=obj, mask=mask,
                                                   line_position=1680, label="default")

    pcv.plot_image(boundary_img1)
    color_histogram = pcv.analyze_color(rgb_img=image, mask=mask, hist_plot_type='all', label="default")
    pcv.plot_image(color_histogram)
    gray_img = pcv.rgb2gray_hsv(rgb_img=image, channel='v')
    pseudocolored_img = pcv.visualize.pseudocolor(gray_img=gray_img, mask=b_fill, cmap='jet')
    pcv.plot_image(pseudocolored_img)
    pcv.print_results(filename="histo_results.txt")




    # roi= pcv.roi.rectangle(img=masked2, x=0,y=0, w=image.shape[0], h=image.shape[1])
    # kept_mask = pcv.roi.filter(mask=b_fill, roi=roi, roi_type='partial')

    #pcv.plot_image(kept_mask)


    # labelo, obj = pcv.create_labels(mask=kept_mask)

    # analysis_image = pcv.analyze.size(img=image, labeled_mask=kept_mask)
    #print("analye object")
    #pcv.plot_image(analysis_image)

    _, ax = plt.subplots(ncols=3, nrows=2, figsize=(16, 9))
    images_to_plot = {
        "Original": cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
        "Gaussian blur": cv2.cvtColor(gaussian_bluri, cv2.COLOR_BGR2RGB),
        "Mask": cv2.cvtColor(masked2, cv2.COLOR_BGR2RGB),
        "ROI Objects": labelo,
        "Analyze object": cv2.cvtColor(analysis_image, cv2.COLOR_BGR2RGB),
        "Pseudolandmarks": cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    }

    for (label, img), axe in zip(images_to_plot.items(), ax.flat):
        axe.imshow(img)
        axe.set_title(label)
        axe.set(xticks=[], yticks=[])
        axe.label_outer()

    #print("pseudolandmarks")
    #plt.imshow(mplimg.imread(image_path))
    top_x, bottom_x, center_v_x = pcv.homology.x_axis_pseudolandmarks(img=image, mask=b_fill, label='default')

    for i in range(len(top_x)):
        plt.scatter(top_x[i][0][0], top_x[i][0][1], c='r', s=10)

    for i in range(len(bottom_x)):
        plt.scatter(bottom_x[i][0][0], bottom_x[i][0][1], c='b', s=10)

    for i in range(len(center_v_x)):
        plt.scatter(center_v_x[i][0][0], center_v_x[i][0][1], c='y', s=10)
    plt.show()

    plot_histogram(image, kept_mask)

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