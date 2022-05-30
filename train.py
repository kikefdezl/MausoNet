from model import mausoNet
import tensorflow as tf
from keras.losses import BinaryCrossentropy
from keras.optimizers import Adam
import os


def main():
    model = mausoNet()
    # model.build((None, 224, 224, 3))

    model.summary()

    model.compile(optimizer=Adam(learning_rate=0.0001), loss=BinaryCrossentropy(), metrics="accuracy")

    dataset_dir = "C:\\Users\\Kike\\Documents\\mausodb"

    train_set = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_dir,
        labels="inferred",
        label_mode="int",
        class_names=None,
        color_mode="rgb",
        batch_size=32,
        image_size=(224, 224),
        shuffle=True,
        seed=7,
        validation_split=0.1,
        subset='training',
        interpolation="bilinear",
        follow_links=False,
        crop_to_aspect_ratio=False,
    )
    val_set = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_dir,
        labels="inferred",
        label_mode="int",
        class_names=None,
        color_mode="rgb",
        batch_size=32,
        image_size=(224, 224),
        shuffle=True,
        seed=7,
        validation_split=0.1,
        subset='validation',
        interpolation="bilinear",
        follow_links=False,
        crop_to_aspect_ratio=False,
    )

    model.fit(train_set, steps_per_epoch=None, epochs=5, validation_data=val_set)
    model.save('mausonet_ckpt.h5')


if __name__ == "__main__":
    main()