import matplotlib.pyplot as plt


def main():

    """
    plot a grid of images with their labels,
    one image for each variety and disease
    """

    _, axs = plt.subplots(2, 4)

    images = {
        "Apple healthy": plt.imread("../images/Apple_healthy/image (1).JPG"),
        "Apple Black rot": plt.imread("../images/Apple_Black_rot/image (1).JPG"),
        "Apple rust": plt.imread("../images/Apple_rust/image (1).JPG"),
        "Apple scab": plt.imread("../images/Apple_scab/image (1).JPG"),
        "Grape healthy": plt.imread("../images/Grape_healthy/image (1).JPG"),
        "Grape Black rot": plt.imread("../images/Grape_Black_rot/image (1).JPG"),
        "Grape Esca": plt.imread("../images/Grape_Esca/image (1).JPG"),
        "Grape spot": plt.imread("../images/Grape_spot/image (1).JPG")
    }

    for ax, (label, img) in zip(axs.flat, images.items()):
        ax.imshow(img)
        ax.set_title(label)
        ax.set(xticks=[], yticks=[])
        ax.label_outer()

    plt.show()


if __name__ == "__main__":
    main()
