import cv2 as cv
import matplotlib.pyplot as plt


def main():

    """
    plot a grid of images with their labels,
    one image for each variety and disease
    """

    _, axs = plt.subplots(2, 4)

    images = {
        "Apple healthy": cv.imread("../images/Apple_healthy/image (1).JPG"),
        "Apple Black rot": cv.imread("../images/Apple_Black_rot/image (1).JPG"),
        "Apple rust": cv.imread("../images/Apple_rust/image (1).JPG"),
        "Apple scab": cv.imread("../images/Apple_scab/image (1).JPG"),
        "Grape healthy": cv.imread("../images/Grape_healthy/image (1).JPG"),
        "Grape Black rot": cv.imread("../images/Grape_Black_rot/image (1).JPG"),
        "Grape Esca": cv.imread("../images/Grape_Esca/image (1).JPG"),
        "Grape spot": cv.imread("../images/Grape_spot/image (1).JPG")
    }

    for i, (ax, (label, img)) in enumerate(zip(axs.flat, images.items())):
        ax.imshow(img)
        ax.set_title(label)
        ax.set(xticks=[], yticks=[])
        ax.label_outer()

    plt.show()


if __name__ == "__main__":
    main()
