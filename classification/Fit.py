import tensorflow as ts
import matplotlib.pyplot as plt
import pickle


def train(directory, model_path, epochs):

    train_ds = ts.keras.utils.image_dataset_from_directory(
        directory,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(256, 256),
        batch_size=50
    )

    val_ds = ts.keras.utils.image_dataset_from_directory(
        directory,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(256, 256),
        batch_size=50
    )

    train_class_names = train_ds.class_names

    num_classes = len(train_class_names)

    model = ts.keras.Sequential([
        ts.keras.layers.Rescaling(1./255),
        ts.keras.layers.Conv2D(32, 30, activation='relu'),
        ts.keras.layers.MaxPooling2D(),
        ts.keras.layers.Conv2D(32, 3, activation='relu'),
        ts.keras.layers.MaxPooling2D(),
        ts.keras.layers.Conv2D(32, 3, activation='relu'),
        ts.keras.layers.MaxPooling2D(),
        ts.keras.layers.Dropout(0.2),
        ts.keras.layers.Flatten(),
        ts.keras.layers.Dense(128, activation='relu'),
        ts.keras.layers.Dense(
            units=num_classes,
            activation='softmax'
        )
    ])

    model.compile(
        optimizer='adam',
        loss=ts.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=['accuracy']
    )

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )

    model.save(model_path)

    with open(model_path + "/class_names.pkl", "wb") as f:
        pickle.dump(train_class_names, f)

    with open(model_path + "/validation_paths.pkl", "wb") as f:
        pickle.dump(val_ds.file_paths, f)

    print("Model saved at : ", model_path)

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    plt.subplot(1, 2, 1)
    plt.title("Accuracy")
    plt.plot(range(epochs), acc, label="train ac")
    plt.plot(range(epochs), val_acc, label="val ac")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.title("loss")
    plt.plot(range(epochs), loss, label="tain loss")
    plt.plot(range(epochs), val_loss, label="val loss")
    plt.legend()

    plt.show()
