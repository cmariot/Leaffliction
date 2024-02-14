import tensorflow as ts
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from numpy import asarray
import sys
import pickle


def train(directory, model_path, epochs):

    # dir -> train_ds, val_ds, test_ds

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
    val_class_names = val_ds.class_names
    print(train_class_names)

    # print(class_names)

    # for images, labels in train_ds.take(1):
    #     for i in range(50):
    #         ax = plt.subplot(10, 5, i + 1)
    #         plt.imshow(images[i].numpy().astype("uint8"))
    #         plt.axis("off")
    #         #print(int(labels[i]))
    #         plt.title(class_names[int(labels[i])], fontsize=8)

    # plt.show()

    # model = ts.keras.Sequential([
    #     ts.keras.layers.Flatten(input_shape=(28, 28)),
    #     ts.keras.layers.Dense(128, activation='relu'),
    #     ts.keras.layers.Dense(10)
    # ])

    num_classes = len(val_class_names)

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
        pickle.dump(val_class_names, f)

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

    # predictions = model.predict(val_ds, verbose=0)
    # print(predictions)

    total_images = 0
    correct = 0

    for data in val_ds:
        pred = model(data)
        print(pred)

    exit()

    for image, labels in val_ds.take(1):

        print("Labels : ", str(labels))

        for i in range(len(labels)):

            print("Image number", i, ":")
            print("Official label :", labels[i])
            print("Predicted label: ", predictions[i])

            # Index 0 : Apple
            # Index 1 : Grape
            if predictions[i][0] >= predictions[i][1]:
                title = "Apple"
            else:
                title = "Grape"

            if (title == "Grape" and labels[i] == 1 ) or (title == "Apple" and labels[i] == 0):
                color = "red"
                correct += 1
            else:
                color = "black"

            plt.title(val_class_names[int(labels[i])] + " prediction : " + title, color=color)
            plt.imshow(image[i].numpy().astype("uint8"))
            plt.show()

            total_images += 1

    print("Total images : ", total_images)
    print("Correct predictions : ", correct)
    print("Accuracy : ", correct / total_images)

    # for image, labels in val_ds.take(1):
    #     for i in range(33):
    #         if predictions[i][0] >= predictions[i][1]:
    #             title = "Apple"
    #         else:
    #             title = "Grape"
    #         if (title == "Grape" and labels[i] == 1 ) or (title == "Apple" and labels[i] == 0):
    #             color = "red"
    #         else:
    #             color = "black"

    #         plt.title(class_names[int(labels[i])] + " prediction : " + title, color=color)
    #         plt.imshow(image[i].numpy().astype("uint8"))
    #         plt.show()

    image = asarray(Image.open(sys.argv[1]))
    topredic = np.expand_dims(image, axis=0)
    pred = model.predict(topredic, verbose=0)
    if (pred[0][0] >= pred[0][1]):
        title = "Grape"
    else:
        title = "Apple"
    plt.title(sys.argv[1] + " Predicted " + title)
    plt.imshow(image)
    plt.show()

    exit()