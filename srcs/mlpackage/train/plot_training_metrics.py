import matplotlib.pyplot as plt


def plot_training_metrics(history, model_path):

    """
    Plot the training metrics
    - Accuracy
    - Loss
    For both the training and validation set
    """

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = len(loss)

    fig, axes = plt.subplots(1, 2, figsize=(16, 9))

    fig.suptitle(
        "Metrics evolution during the training",
        fontsize=13,
        fontweight="bold"
    )

    # Axes[0] is the loss
    axes[0].plot(range(epochs), loss, label="Train loss")
    axes[0].plot(range(epochs), val_loss, label="Validation loss")
    axes[0].set_title("Evolution of the loss during the training")
    axes[0].set_xlabel("Epochs")
    axes[0].set_xticks(range(0, epochs, 1))
    axes[0].set_ylabel("Loss")
    axes[0].legend()
    axes[0].grid(
        linestyle="--",
        linewidth=0.5
    )

    # Axes[1] is the accuracy
    axes[1].plot(range(epochs), acc, label="Train accuracy")
    axes[1].plot(range(epochs), val_acc, label="Validation accuracy")
    axes[1].set_title("Evolution of the accuracy during the training")
    axes[1].set_xlabel("Epochs")
    axes[1].set_xticks(range(0, epochs, 1))
    axes[1].set_ylabel("Accuracy")
    axes[1].legend()
    axes[1].set_ylim(bottom=0, top=1)
    axes[1].grid(
        linestyle="--",
        linewidth=0.5
    )

    plt.savefig(model_path + "/plot.png")

    plt.show()
