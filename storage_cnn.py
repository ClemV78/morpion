import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

n_cercle = n_croix = 80
train_images, train_labels, test_images, test_labels = [], [], [], []


def importation_images():
    for i in range(n_cercle):
        train_images.append(plt.imread("images_cercle/cercle" +
                                       str(i)+".jpeg")[:, :, 0])
        train_labels.append(0)
    for i in range(n_croix):
        train_images.append(plt.imread("images_croix/cross" +
                                       str(i)+".jpeg")[:, :, 0])
        train_labels.append(1)
    for i in range(n_cercle, n_cercle+10):
        test_images.append(plt.imread("images_cercle/cercle" +
                                      str(i)+".jpeg")[:, :, 0])
        test_labels.append(0)
    for i in range(n_croix, n_croix+10):
        test_images.append(plt.imread("images_croix/cross" +
                                      str(i)+".jpeg")[:, :, 0])
        test_labels.append(1)


importation_images()
# A remplir
(train_images, train_labels), (test_images,
                               test_labels) = (np.array(train_images), np.array(train_labels)), (np.array(test_images), np.array(test_labels))

train_images = train_images.reshape(-1, 28 * 28) / 255.0
test_images = test_images.reshape(-1, 28 * 28) / 255.0


# Define a simple sequential model


def create_model():
    model = tf.keras.models.Sequential([
        keras.layers.Dense(512, activation='relu', input_shape=(784,)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(2)
    ])

    model.compile(optimizer='adam',
                  loss=tf.losses.SparseCategoricalCrossentropy(
                      from_logits=True),
                  metrics=[tf.metrics.SparseCategoricalAccuracy()])

    return model


# Create a basic model instance
model = create_model()

# Display the model's architecture
model.summary()


# Train the model with the new callback
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(
                  from_logits=True),
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, epochs=20,
                    validation_data=(test_images, test_labels))

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')
plt.show()

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

model.save('model_morpion.h5')
