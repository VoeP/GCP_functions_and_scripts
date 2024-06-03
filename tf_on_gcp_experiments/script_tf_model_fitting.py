# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 11:33:30 2024

@author: volte
"""
from google.cloud import bigquery
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import TextVectorization
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import re
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


# Initialize a BigQuery client
client = bigquery.Client()

# Define your query
query = """
SELECT review, label 
FROM `ml-deployments-practice.sparse_features_demo.processed_reviews`
"""

df = client.query(query).to_dataframe()

def preprocess_text(text):
    text = text.lower()
    text = text.replace("<br />", " ")
    text = ''.join([c if c.isalpha() or c.isspace() else ' ' for c in text])
    text = text.strip()
    return text


def convert_to_labels(text):
    return 0 if text == 'Negative' else 1

df['preproc_text'] = df['review'].apply(preprocess_text)
df['label'] = df['label'].apply(convert_to_labels)

X = df['review']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X,y,  test_size=0.2, random_state=42)

X_test, X_val, y_test, y_val = train_test_split(
    X_train, y_train, test_size=0.5, random_state=42
)

# Hyperparameters
vocab_size = 10000
max_length = 100

# Create the TextVectorization layer
vectorizer = TextVectorization(max_tokens=vocab_size, output_mode='int', output_sequence_length=max_length, pad_to_max_tokens=True)

# Adapt the vectorizer to the training data
vectorizer.adapt(X_train)
vectorizer(X_train.iloc[0])


#current
model = tf.keras.models.Sequential([
   # keras.layers.Reshape(None,),
    tf.keras.layers.InputLayer(input_shape=[1], dtype="string"),
    vectorizer,
    tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=16, input_length=max_length),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(20, return_sequences=True)),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(20)),
    tf.keras.layers.Dense(6, activation='relu'),
    #tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.summary()


#Create trainnig dataset
batch_size= 100
train_ds = tf.data.Dataset.from_tensor_slices((X_train, y_train))
train_ds = train_ds.shuffle(buffer_size=len(X_train)).batch(batch_size)

# Create validation dataset
val_ds = tf.data.Dataset.from_tensor_slices((X_val, y_val))
val_ds = val_ds.batch(batch_size)

model.compile(optimizer='adam', 
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
              metrics=['accuracy'])

history = model.fit(train_ds, validation_data=val_ds, epochs = 10)


test_ds = tf.data.Dataset.from_tensor_slices((X_test, y_test))
test_ds = test_ds.batch(batch_size)
test_loss, test_acc = model.evaluate(test_ds)
print('\nTest accuracy: {}'.format(test_acc))


#Plot evolution of accuracy over epochs
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('acc_and_val_accuracy.png')
plt.close()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('loss.png')
plt.close()

model.save('model_draft.keras')