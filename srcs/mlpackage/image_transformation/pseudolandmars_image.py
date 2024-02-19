from plantcv import plantcv as pcv


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
    Replace the pixels of 'image' by the color by a circle centered on the
    pseudolandmarks
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
