import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense, Dropout
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from results import save

vocab_size = 1000

(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=vocab_size)

#Pad sequences to have the same length
max_length = 100
x_train = pad_sequences(x_train, maxlen=max_length, padding='post')
x_test = pad_sequences(x_test, maxlen=max_length, padding='post')

model = Sequential()

#Add an Embedding layer for word embeddings
embedding_dim = 50
model.add(Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length))

#Flatten the 3D embedding tensor to 2D
model.add(Flatten())

model.add(Dense(units=1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

training = model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))

x = [i for i in range(10)]
save("tensor","mlp_acc",x,training.history['val_accuracy'],training.history['accuracy'],"test")
save("tensor","mlp_loss",x,training.history['val_loss'],training.history['loss'],"test")