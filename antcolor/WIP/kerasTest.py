import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt


fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
#this one is already ready- normally have to divide between train, test, trainlabels, testlabels before loading

train_images = train_images /255.0
test_images = test_images /255.0

model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28,28)), #flatten
        keras.layers.Dense(128,activation=tf.nn.relu), #128 nodes in hidden layer
        keras.layers.Dense(10,activation=tf.nn.softmax) #10 output nodes 1 for each class
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=5)

test_lost, test_accuracy = model.evaluate(test_images,test_labels)

plt.figure()
plt.xticks()
plt.yticks()
plt.imshow(train_images[3])
plt.colorbar()
