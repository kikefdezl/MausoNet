import numpy as np
import tensorflow as tf


def get_data():
    batch_size = 32
    image_size = (512, 512)

    ds_dir = '/media/kike/HDD/MULTIMEDIA/MausoNet_dataset/split/trainval'

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        ds_dir,
        validation_split=0.2,
        subset="training",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size,
    )

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        ds_dir,
        validation_split=0.2,
        subset="validation",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size,
    )
    pass
    return train_ds, val_ds


def train():
    epochs = 2

    train_ds, val_ds = get_data()

    model = tf.keras.models.Sequential(
        [tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(512, 512, 3)),
         tf.keras.layers.MaxPool2D(),
         tf.keras.layers.Conv2D(64, 3, activation='relu'),
         tf.keras.layers.MaxPool2D(),
         tf.keras.layers.Conv2D(128, 3, activation='relu'),
         tf.keras.layers.MaxPool2D(),
         tf.keras.layers.Conv2D(256, 3, activation='relu'),
         tf.keras.layers.Flatten(),
         tf.keras.layers.Dense(1, activation='sigmoid')]
    )

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint("save_at_{epoch}.h5"),
    ]

    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss=tf.keras.losses.BinaryCrossentropy(),
        metrics=['accuracy']
    )

    model.summary()

    model.fit(train_ds, epochs=epochs, callbacks=callbacks, validation_data=val_ds)


if __name__ == "__main__":
    train()
