from matplotlib import pyplot as plt


def plot_images(images: dict, path) -> None:

    """
    Plot the original images and the augmented ones, on a grid
    """

    # Grid size
    nb_images = len(images)
    nb_rows = 2
    nb_cols = nb_images // nb_rows

    _, axs = plt.subplots(nb_rows, nb_cols, figsize=(16, 9))

    for ax, (key, value) in zip(axs.flat, images.items()):

        ax.imshow(value)
        ax.set_title(key)
        ax.set(xticks=[], yticks=[])
        ax.label_outer()

    plt.suptitle(
        f"Preview of the augmentations on {path}",
        fontweight="bold",
        y=0.05
    )

    plt.show()
