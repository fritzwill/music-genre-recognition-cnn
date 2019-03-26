from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from keras.datasets import mnist
from keras.utils import to_categorical
from keras.preprocessing import image
from sklearn.model_selection import train_test_split
import os
import numpy as np
import pandas as pd


def get_train_test():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    ClassDict = {'Pop': 0,
                'Instrumental': 1,
                'Hip-Hop': 2,
                'Experimental': 3,
                'Electronic': 4,
                'Folk': 5,
                'Rock': 6,
                'International': 7}
    
    x_train = list()
    y_train = list()
    
    rootDir = '/home/group/ai-fa18-project/willSpect/'
    for k, v in ClassDict.items():
        i = 0
        for currentDir, subdirList, fileList in os.walk(rootDir+k):
            for png in fileList:
                if i > 500:
                    break
                i+=1
                sampleImage = image.load_img(currentDir+'/'+png, target_size = (128, 128))
                sampleImage = image.img_to_array(sampleImage)
                
                x_train.append(sampleImage)
                y_train.append(ClassDict[currentDir.split('/')[-1]])

    train_x, test_x, train_y, test_y = train_test_split(np.array(x_train), to_categorical(np.array(y_train)), random_state=42)
    return train_x, test_x, train_y, test_y

def create_model(train_x, test_x, train_y, test_y):
    model = Sequential()
    model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(128,128, 3)))

    model.add(Conv2D(32, kernel_size=3, activation='relu'))
    model.add(Flatten())
    model.add(Dense(8, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=3)
