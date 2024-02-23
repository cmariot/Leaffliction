import matplotlib.pyplot as plt
import pickle
from keras import Sequential, layers, losses, callbacks, optimizers
from keras.utils import image_dataset_from_directory


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


def save_model(model, model_path, train_class_names, validation_paths_lst):

    """
    Save the trained model and the class names
    """

    model.save(model_path)

    with open(model_path + "/class_names.pkl", "wb") as f:
        pickle.dump(train_class_names, f)

    with open(model_path + "/validation_paths.pkl", "wb") as f:
        pickle.dump(validation_paths_lst, f)

    print("Model saved at : ", model_path)


def set_validation_paths(
    val_ds,
    is_augmented,
    is_transformed,
    transformation_dir: str,
    original_dir
):

    """
    Transform the validation paths to the original paths
    Will be saved in a pickle file, used for the prediction
    """

    if not is_transformed and not is_augmented:
        return

    if transformation_dir[-1] == "/":
        transformation_dir = transformation_dir[:-1]

    validation_paths_lst = []
    for path in val_ds.file_paths:
        path = path.replace(transformation_dir, original_dir, 1)
        slash_index = path.rfind("/")
        if slash_index != -1:
            filename = path[slash_index + 1:]
        extension_index = path.rfind(".")
        extension = path[extension_index:]
        for i in range(is_augmented + is_transformed):
            underscore_index = filename.rfind("_")
            if underscore_index == -1:
                break
            else:
                filename = filename[:underscore_index]
            path = path[:slash_index + 1] + filename
        path = path + extension
        validation_paths_lst.append(path)
    return validation_paths_lst


def train(
    directory,
    model_path,
    epochs,
    is_augmented,
    is_transformed,
    original_dir
):

    GREEN = "\033[92m"
    RESET = "\033[0m"
    print(f"{GREEN}Training phase :{RESET}\n")

    train_ds = image_dataset_from_directory(
        directory,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(256, 512),
        batch_size=10
    )

    val_ds = image_dataset_from_directory(
        directory,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(256, 512),
        batch_size=256
    )

    train_class_names = train_ds.class_names

    num_classes = len(train_class_names)

    callback = callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10
    )

    model = Sequential([

        layers.Rescaling(1./255),
        layers.Conv2D(
            filters=128,
            kernel_size=4,
            activation='relu'
        ),
        layers.MaxPooling2D(),

        layers.Conv2D(
            filters=64,
            kernel_size=4,
            activation='relu'
        ),
        layers.MaxPooling2D(),

        layers.Conv2D(
            filters=32,
            kernel_size=4,
            activation='relu'
        ),
        layers.MaxPooling2D(),

        layers.Conv2D(
            filters=16,
            kernel_size=4,
            activation='relu'
        ),
        layers.MaxPooling2D(),

        # layers.Dropout(0.1),

        layers.Flatten(),

        layers.Dense(
            units=128,
            activation='relu'
        ),
        layers.Dense(
            units=num_classes,
            activation='softmax'
        )
    ])

    model.build(
        input_shape=(None, 256, 512, 3)
    )

    print(model.summary())

    adam = optimizers.legacy.Adam()

    model.compile(
        optimizer=adam,
        loss=losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=['accuracy']
    )

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[callback],
        use_multiprocessing=True
    )

    validation_paths_lst = set_validation_paths(
        val_ds,
        is_augmented,
        is_transformed,
        directory,
        original_dir
    )
    save_model(model, model_path, train_class_names, validation_paths_lst)

    plot_training_metrics(history, model_path)
