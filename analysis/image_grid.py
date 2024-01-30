import cv2 as cv
import matplotlib.pyplot as plt


def main():

    """
    plot a grid of images with their labels,
    one image for each variety and disease
    """

    _, axs = plt.subplots(2, 4)

    imgs = [
        cv.imread("../images/Apple_Black_rot/image (1).JPG"),
        cv.imread("../images/Apple_healthy/image (1).JPG"),
        cv.imread("../images/Apple_rust/image (1).JPG"),
        cv.imread("../images/Apple_scab/image (1).JPG"),
        cv.imread("../images/Grape_Black_rot/image (1).JPG"),
        cv.imread("../images/Grape_Esca/image (1).JPG"),
        cv.imread("../images/Grape_healthy/image (1).JPG"),
        cv.imread("../images/Grape_spot/image (1).JPG")
    ]

    labels = [
        "Apple Black rot",
        "Apple healthy",
        "Apple rust",
        "Apple scab",
        "Grape Black rot",
        "Grape Esca",
        "Grape healthy",
        "Grape spot"
    ]

    for i, ax in enumerate(axs.flat):
        ax.imshow(imgs[i])
        ax.set_title(labels[i])
        ax.set(xticks=[], yticks=[])
        ax.label_outer()

    plt.show()


if __name__ == "__main__":
    main()
