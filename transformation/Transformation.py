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


def display_transformations(image_path, dest, options):

    # Read the image
    image, path, name = pcv.readimage(image_path)

    # Display the original image
    pcv.plot_image(image)

    #  We want to remove as much background as possible without loosing any information about the plant

    # Convert the image to grayscale by extracting the saturation channel
    s = pcv.rgb2gray_hsv(
        rgb_img=image,
        channel='s'
    )
    pcv.plot_image(s)

    # Threshold the grayscaled image
    s_thresh = pcv.threshold.binary(
        gray_img=s,
        threshold=60,
        object_type='light'
    )
    pcv.plot_image(s_thresh)







def main():



    # for key, value in transformations.items():
    #     print(key)
    #     transformed_image = value(image)
    #     pcv.plot_image(transformed_image)
    path, dest, options = parse_argument()

    image, path, name = pcv.readimage(path)
    s = pcv.rgb2gray_hsv(rgb_img=image, channel='s')
    pcv.plot_image(s)
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, object_type='light')
    #pcv.plot_image(s_thresh)
    s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
    #pcv.plot_image(s_mblur)
    gaussian_bluri = pcv.gaussian_blur(img=s_thresh, ksize=(3, 3), sigma_x=0, sigma_y=None)
    #pcv.plot_image(gaussian_bluri)

    b = pcv.rgb2gray_lab(rgb_img=image, channel='b')
    #pcv.plot_image(b)

    b_thresh=pcv.threshold.binary(gray_img=b, threshold=135,object_type='light')

    bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_thresh)
    #pcv.plot_image(bs)

    masked = pcv.apply_mask(img=image, mask=bs, mask_color='white')
    #pcv.plot_image(masked)

    masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
    masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')

    #pcv.plot_image(masked_a)
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
    pcv.plot_image(ab_fill)
    #pcv.plot_image(ab_fill)
    closed_ab = pcv.closing(gray_img=ab_fill)
    #pcv.plot_image(gray_img=ab_fill)
    masked2= pcv.apply_mask(img=masked, mask=ab_fill, mask_color='white')
    pcv.plot_image(masked2)

    #obj_hierachy= pcv.find_objects(img=masked2, mask=ab_fill)

    #roi1, roi_hierarchy = pcv.roi.rectangle(img=masked2, x=(image.shape[0] * 0.1), y=(image.shape[1] * 0.1), w=(image.shape[0] * 0.9), h=(image.shape[1] * 0.9))
    roi= pcv.roi.rectangle(img=masked2, x=0,y=0, w=image.shape[0], h=image.shape[1])
    kept_mask = pcv.roi.filter(mask=ab_fill, roi=roi, roi_type='partial')
    #pcv.plot_image(filtered)
    analysis_image = pcv.analyze.size(img=image, labeled_mask=kept_mask)
    print("analysis")
    pcv.plot_image(analysis_image)


    color_histogram = pcv.analyze.color(rgb_img=image, colorspaces="all", labeled_mask=kept_mask,label="default")
    #pcv.plot_image(color_histogram)
    #print(color_histogram)
    res = pcv.outputs.save_results("histo")
    #print(list(pcv.outputs.observations['default_1']['saturation_frequencies'].keys()))
    print(pcv.outputs.observations['default_1']['blue_frequencies']['value'])
    print(pcv.outputs.observations['default_1']['blue_frequencies']['label'])

    y = pcv.outputs.observations['default_1']['blue_frequencies']['value']
    x = pcv.outputs.observations['default_1']['blue_frequencies']['label']

    plt.plot(x, y, label="blue")

    y = pcv.outputs.observations['default_1']['green_frequencies']['value']
    x = pcv.outputs.observations['default_1']['green_frequencies']['label']
    plt.plot(x, y, label="green")
    y = pcv.outputs.observations['default_1']['red_frequencies']['value']
    x = pcv.outputs.observations['default_1']['red_frequencies']['label']
    plt.plot(x, y, label="red")
    plt.legend()
    plt.show()
    hue_cir = pcv.outputs.observations['default_1']['hue_frequencies']
    print(list(hue_cir.keys()))
    #print(hue_cir)
    pcv.print_image(img=color_histogram, filename="histo.png")


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