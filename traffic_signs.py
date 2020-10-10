# -*- coding: utf-8 -*-
"""Traffic Signs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p_LUDDOuvFY0GRhecIyxq-yUYviuPWFQ
"""

!git clone https://bitbucket.org/jadslim/german-traffic-signs

!ls german-traffic-signs

import numpy as np
import cv2
import keras
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils.np_utils import to_categorical
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers import Dropout
import pickle
import pandas as pd
import random



np.random.seed(0)

with open('german-traffic-signs/train.p', 'rb') as f:
  train_data=pickle.load(f)
with open('german-traffic-signs/valid.p', 'rb') as f:
  val_data=pickle.load(f)
with open('german-traffic-signs/test.p', 'rb') as f:
  test_data=pickle.load(f)

print(type(train_data))

X_train, y_train = train_data['features'], train_data['labels']
X_val, y_val = val_data['features'], val_data['labels']
X_test , y_test = test_data['features'], test_data['labels']

print(X_train.shape)
print(X_val.shape)
print(X_test.shape)

assert(X_train.shape[0]==y_train.shape[0]), "The number of images is not equal to number of labels"
assert(X_test.shape[0]==y_test.shape[0]),"The number of images is not equal to number of labels"
assert(X_train.shape[1:]==(32,32,3)), "The dimensions of the images are not 28x28"
assert(X_test.shape[1:]==(32,32,3)),"The dimensions of the images are not 28x28"

data = pd.read_csv('german-traffic-signs/signnames.csv')

num_of_samples=[]

cols=5
num_classes=43

fig, axs=plt.subplots(nrows=num_classes,ncols=cols, figsize=(5,50))
fig.tight_layout()
for i in range(cols):
    for j, row in data.iterrows():
        x_selected=X_train[y_train==j]
        axs[j][i].imshow(x_selected[random.randint(0,len(x_selected-1)),:,:] ,cmap=plt.get_cmap("gray"))
        axs[j][i].axis("off")
        if i==2:
            axs[j][i].set_title(str(j) + "-" + row["SignName"])
            num_of_samples.append(len(x_selected))

print(num_of_samples)
plt.figure(figsize=(12,4))
plt.bar(range(0,num_classes), num_of_samples)
plt.title("Distribution of the training dataset")
plt.xlabel("Class number")
plt.ylabel("Number of images")

plt.imshow(X_train[1000])
plt.axis('off')
print(X_train[1000].shape)
print(y_train[1000])

def grayscale(img):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  return gray

img = grayscale(X_train[1000])
plt.imshow(img)
plt.axis("off")
print(img.shape)

def equalize(img):
  img = cv2.equalizeHist(img)
  return img

img  = equalize(img)
plt.imshow(img)
plt.axis("off")
print(img.shape)

def preprocessing(img):
  img = grayscale(img)
  img = equalize(img)
  img = img/255
  return img

X_train = np.array(list(map(preprocessing, X_train)))
X_val = np.array(list(map(preprocessing, X_val)))
X_test = np.array(list(map(preprocessing, X_test)))

X_train=X_train.reshape(34799, 32,32, 1)
X_test=X_test.reshape(12630, 32,32, 1)
X_val=X_val.reshape(4410, 32,32, 1)
print(X_train.shape)

y_train=to_categorical(y_train, 43)
y_test=to_categorical(y_test,43)
y_val=to_categorical(y_val,43)

def leNet_model():
  model=Sequential()
  model.add(Conv2D(60, (5,5), input_shape=(32,32,1), activation='relu'))
  model.add(Conv2D(60, (5,5), activation='relu'))
  model.add(MaxPooling2D(pool_size=(2,2)))
  model.add(Conv2D(30,(3,3), activation='relu'))
  model.add(Conv2D(30,(3,3), activation='relu'))
  model.add(MaxPooling2D(pool_size=(2,2)))
  model.add(Dropout(0.5))
  model.add(Flatten())
  model.add(Dense(500,activation='relu'))
  model.add(Dropout(0.5))
  model.add(Dense(num_classes, activation='softmax'))
  model.compile(Adam(lr=0.001), loss='categorical_crossentropy',metrics=['accuracy'])
  return model

model=leNet_model()
print(model.summary())

history=model.fit(X_train, y_train, validation_data=(X_val, y_val),epochs=10,batch_size=400,verbose=1,shuffle=1)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['loss','val_loss'])
plt.title('loss')
plt.xlabel('epoch')

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(['acc','val_accuracy'])
plt.title('Accuracy')
plt.xlabel('epoch')

