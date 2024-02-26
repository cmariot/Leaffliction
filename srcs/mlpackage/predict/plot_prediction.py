import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from numpy import asarray
from PIL import Image


def plot_prediction(
    y: str,
    y_hat: str,
    y_pred: list,
    class_names: list,
    image,
    image_path: str
):

    gs = gridspec.GridSpec(2, 4)
    plt.figure(figsize=(16, 9))
    gs.update(wspace=0.5)

    ax1 = plt.subplot(gs[0, :2])
    ax2 = plt.subplot(gs[0, 2:])
    ax3 = plt.subplot(gs[1, 1:3])

    # Original image and transformed image
    ax1.set_title("Original image")
    ax1.imshow(asarray(Image.open(image_path)))
    ax1.axis('off')

    ax2.set_title("Transformed image used for prediction")
    ax2.imshow(image)
    ax2.axis('off')

    # Bar plot of the predictions probabilities
    ax3.set_title("Predictions probabilities for each class")
    ax3.barh(y=class_names, width=y_pred[0], height=0.2)
    ax3.set_yticks(range(len(class_names)))
    ax3.set_yticklabels(class_names)
    ax3.set_xlabel("Probability")
    ax3.set_ylabel("Class")
    ax3.set_xlim([0, 1])
    for i, v in enumerate(y_pred[0]):
        ax3.text(v, i, f"{v:.2f}", ha="left", va="center")

    if y in class_names:

        title = f"Class predicted: {y_hat}\nOriginal class: {y}"
        if y == y_hat:
            color = "green"
        else:
            color = "red"

    else:

        title = f"Class predicted: {y_hat}"
        color = 'black'

    # Title at the Axes[1, 1] position
    plt.suptitle(
        title,
        y=0.95,
        fontsize=13,
        fontweight="bold",
        ha="center",
        va="center",
        color=color
    )

    plt.show()
    plt.close()
