import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

new_model = tf.keras.models.load_model('model_morpion.h5')


def prediction(path):
    img = plt.imread(path)
    img = img[:, :, 0]
    img = img.reshape(-1, 28 * 28) / 255.0
    a = new_model.predict([img])
    if a[0][0] > a[0][1]:
        return(0)
    return(1)


if __name__ == "__main__":
    print(prediction('images_test/cross8.jpeg'))
