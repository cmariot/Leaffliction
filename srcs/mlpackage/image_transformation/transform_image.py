import cv2
from plantcv import plantcv as pcv
import rembg
import matplotlib.pyplot as plt
from .roi_image import create_roi_image
from .pseudolandmars_image import create_pseudolandmarks_image
from .color_histogram import plot_histogram


def get_image_name(new_path, label):

    """
    Return the name of the image to save
    """

    point_index = new_path.rfind(".")
    label = label.replace(" ", "_")
    if point_index != -1:
        return new_path[:point_index] + "_" + label + new_path[point_index:]
    else:
        return new_path + "_" + label


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
    gaussian_blur = pcv.gaussian_blur(img=filled, ksize=(3, 3))

    # Apply a mask to the image
    masked = pcv.apply_mask(img=image, mask=gaussian_blur, mask_color='black')

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

    pseudowithoutbg = create_pseudolandmarks_image(
        masked, kept_mask
    )

    double = cv2.hconcat([masked, pseudolandmarks])
    doublewithoutbg = cv2.hconcat([masked, pseudowithoutbg])

    images = {
        "Original": cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
        "Gaussian blur": cv2.cvtColor(gaussian_blur, cv2.COLOR_BGR2RGB),
        "Mask": cv2.cvtColor(masked, cv2.COLOR_BGR2RGB),
        "ROI Objects": cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB),
        "Analyze object": cv2.cvtColor(analysis_image, cv2.COLOR_BGR2RGB),
        "Pseudolandmarks": cv2.cvtColor(pseudolandmarks, cv2.COLOR_BGR2RGB),
        "Pseudowithoutbg": cv2.cvtColor(pseudowithoutbg, cv2.COLOR_BGR2RGB),
        "Double": cv2.cvtColor(double, cv2.COLOR_BGR2RGB),
        "Doublewithoutbg": cv2.cvtColor(doublewithoutbg, cv2.COLOR_BGR2RGB)
    }

    # Used in predict.py to return the transformed images
    if is_launch_on_dir is None:
        [images.pop(key) for key in images.keys() - options]
        return images

    # If the argument of the program is a file, display the transformation
    if not is_launch_on_dir:

        # Create the figure to plot
        fig, ax = plt.subplots(ncols=3, nrows=3, figsize=(16, 9))

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
