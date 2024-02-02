# https://plantcv.readthedocs.io/en/v3.4.1/vis_tutorial/

import argparse
from plantcv import plantcv as pcv
import plantcv as pcv2
import os
import matplotlib.pyplot as plt
import seaborn as sns


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


def plot_stat_hist(label, sc=1):

    y = pcv.outputs.observations['default_1'][label]['value']
    x = [i * sc for i in  pcv.outputs.observations['default_1'][label]['label']]

    if label == "hue_frequencies":
        x = x[:int(255 / 2)]
        y = y[:int(255 / 2)]
    if label == "blue-yellow_frequencies" or label == "green-magenta_frequencies":
        x = [x + 128 for x in x]

    plt.plot(x, y, label=label)

def display_transformations(image_path, dest, options):

    # pcv.params.debug = "plot"

    image, path, name = pcv.readimage(image_path)
    s = pcv.rgb2gray_hsv(rgb_img=image, channel='s')
    pcv.plot_image(s)
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, object_type='light')
    #pcv.plot_image(s_thresh)
    s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
    pcv.plot_image(s_mblur)
    gaussian_bluri = pcv.gaussian_blur(img=s_thresh, ksize=(3, 3), sigma_x=0, sigma_y=None)
    #pcv.plot_image(gaussian_bluri)

    b = pcv.rgb2gray_lab(rgb_img=image, channel='b')
    pcv.plot_image(b)

    b_thresh=pcv.threshold.binary(gray_img=b, threshold=135,object_type='light')

    bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_thresh)
    pcv.plot_image(bs)

    masked = pcv.apply_mask(img=image, mask=bs, mask_color='white')
    pcv.plot_image(masked)

    masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
    masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')

    pcv.plot_image(masked_a)
    #pcv.plot_image(masked_b)

    maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, object_type='dark')
    maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135, object_type='light')
    maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=135, object_type='light')

    #pcv.plot_image(maskeda_thresh)
    #pcv.plot_image(maskeda_thresh1)
    #pcv.plot_image(maskedb_thresh)

    ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
    ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)

    # pcv.plot_image(ab1)
    # pcv.plot_image(ab)

    opened_ab = pcv.opening(gray_img=ab)
    #pcv.plot_image(opened_ab)

    xor_img = pcv.logical_xor(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
    #pcv.plot_image(xor_img)

    ab_fill = pcv.fill(bin_img=ab, size=200)
    print("fill")
    # pcv.plot_image(ab_fill)
    #pcv.plot_image(ab_fill)
    closed_ab = pcv.closing(gray_img=ab_fill)
    #pcv.plot_image(gray_img=ab_fill)
    masked2= pcv.apply_mask(img=masked, mask=ab_fill, mask_color='white')
    # pcv.plot_image(masked2)

    #obj_hierachy= pcv.find_objects(img=masked2, mask=ab_fill)

    #roi1, roi_hierarchy = pcv.roi.rectangle(img=masked2, x=(image.shape[0] * 0.1), y=(image.shape[1] * 0.1), w=(image.shape[0] * 0.9), h=(image.shape[1] * 0.9))
    roi= pcv.roi.rectangle(img=masked2, x=0,y=0, w=image.shape[0], h=image.shape[1])
    kept_mask = pcv.roi.filter(mask=ab_fill, roi=roi, roi_type='partial')
    #pcv.plot_image(filtered)`
    analysis_image = pcv.analyze.size(img=image, labeled_mask=kept_mask)
    print("analysis")
    # pcv.plot_image(analysis_image)
    #print(vars(pcv))

    print("DTYPE:", bs.dtype)

    import cv2

    import numpy as np

    # Create a new array, filled with the 2 first dimensions of image

    arr = np.zeros((masked2.shape[0], masked2.shape[1]), dtype=np.uint8)
    for i in range(masked2.shape[0]):
        for j in range(masked2.shape[1]):
            arr[i][j] = masked2[i][j][1]
    print("SAHPE :", arr.shape)

    img, _, _ = pcv.readimage(image_path)
    top_x, bottom_x, center_v_x = pcv.homology.x_axis_pseudolandmarks(img=analysis_image, mask=arr, label='default')
    top_y, bottom_y, center_v_y = pcv.homology.y_axis_pseudolandmarks(img=analysis_image, mask=arr, label='default')

    print("TOP X:", top_x)
    print("TOP Y:", top_y)

    plt.imshow(arr, cmap='gray')

    for i in range(len(top_x)):
        plt.scatter(top_x[i][0][0], top_x[i][0][1], c='r', s=10)

    for i in range(len(top_y)):
        plt.scatter(top_y[i][0][0], top_y[i][0][1], c='r', s=10)

    for i in range(len(bottom_x)):
        plt.scatter(bottom_x[i][0][0], bottom_x[i][0][1], c='b', s=10)

    for i in range(len(bottom_y)):
        plt.scatter(bottom_y[i][0][0], bottom_y[i][0][1], c='b', s=10)

    for i in range(len(center_v_x)):
        plt.scatter(center_v_x[i][0][0], center_v_x[i][0][1], c='g', s=10)

    for i in range(len(center_v_y)):
        plt.scatter(center_v_y[i][0][0], center_v_y[i][0][1], c='g', s=10)


    # for i in range(len(bottom)):
        # plt.scatter(bottom[i][0][0], bottom[i][0][1], c='b', s=10)
#
    # for i in range(len(center_v)):
        # plt.scatter(center_v[i][0][0], center_v[i][0][1], c='g', s=10)
#
    plt.show()





    color_histogram = pcv.analyze.color(rgb_img=image, colorspaces="all", labeled_mask=kept_mask,label="default")
    #print(color_histogram)
    res = pcv.outputs.save_results("histo")
    #print(list(pcv.outputs.observations['default_1']['saturation_frequencies'].keys()))
    print(pcv.outputs.observations['default_1']['blue_frequencies']['value'])
    print(f"SUM = {sum(pcv.outputs.observations['default_1']['lightness_frequencies']['value'])}")


    dict_label = {"blue_frequencies" : 1, "green_frequencies": 1, "green-magenta_frequencies" : 1 , "lightness_frequencies" : 2.55, "red_frequencies" : 1, "blue-yellow_frequencies" : 1, "hue_frequencies" : 1, "saturation_frequencies" : 2.55, "value_frequencies" : 2.55}

    for key, val in dict_label.items():
        plot_stat_hist(key, val)
    plt.legend()
    plt.show()
    hue_cir = pcv.outputs.observations['default_1']['hue_frequencies']
    print(list(hue_cir.keys()))
    #print(hue_cir)
    pcv.print_image(img=color_histogram, filename="histo.png")


    homolog_pts, start_pts, stop_pts, ptvals, chain, max_dist = pcv.homology.acute(img=img,
                                                                               mask=arr, win=42,
                                                                               threshold=130)
    img_plms = image.copy()
    cv2.drawContours(img_plms, homolog_pts, -1, (255, 255, 255), pcv.params.line_thickness)


    pcv.plot_image(img_plms)
    plm_fig=plt.figure(figsize=(7, 10))
    plm_fig=plt.imshow(img_plms)
    plm_fig=plt.xscale('linear')
    plm_fig=plt.axis('off')
    plt.show()




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
    except Exception as error:
        print(error)
        exit(1)