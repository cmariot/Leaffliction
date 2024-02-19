from plantcv import plantcv as pcv


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
