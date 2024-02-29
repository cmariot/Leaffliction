from keras import Sequential
from keras.utils import image_dataset_from_directory
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, Rescaling
from keras.optimizers.legacy import Adam
from keras.losses import SparseCategoricalCrossentropy
from keras.callbacks import EarlyStopping

from .train.plot_training_metrics import plot_training_metrics
from .train.save_model import save_model
from .train.set_validation_paths import set_validation_paths
from .colors_variable import GREEN, RESET


def train(
    directory,
    model_path,
    epochs,
    is_augmented,
    is_transformed,
    original_dir
):

    print(f"{GREEN}Training phase :{RESET}\n")

    train_ds = image_dataset_from_directory(
        directory,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(256, 512),
        batch_size=64
    )

    val_ds = image_dataset_from_directory(
        directory,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(256, 512),
        batch_size=64
    )

    train_class_names = train_ds.class_names

    num_classes = len(train_class_names)

    model = Sequential([

        Rescaling(1./255),

        Conv2D(
            filters=16,
            kernel_size=4,
            activation='relu'
        ),
        MaxPooling2D(),

        Conv2D(
            filters=32,
            kernel_size=4,
            activation='relu'
        ),
        MaxPooling2D(),

        Dropout(0.1),

        Conv2D(
            filters=64,
            kernel_size=4,
            activation='relu'
        ),
        MaxPooling2D(),

        Conv2D(
            filters=128,
            kernel_size=4,
            activation='relu'
        ),
        MaxPooling2D(),
        Dropout(0.1),

        Flatten(),

        Dense(
            units=128,
            activation='relu'
        ),
        Dropout(0.1),

        Dense(
            units=num_classes,
            activation='softmax'
        )
    ])

    model.build(
        input_shape=(None, 256, 512, 3)
    )

    print(model.summary())

    model.compile(
        optimizer=Adam(),
        loss=SparseCategoricalCrossentropy(from_logits=False),
        metrics=['accuracy']
    )

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[
            EarlyStopping(
                monitor='val_loss',
                patience=10
            )
        ],
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
