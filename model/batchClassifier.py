from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from keras.datasets import mnist
from keras.utils import to_categorical, Sequence
from keras.preprocessing import image
from sklearn.model_selection import train_test_split
from skimage.io import imread
from skimage.transform import resize
import os
import numpy as np
import pandas as pd

class DataGenerator(Sequence):
    def __init__(self, images, genres, batch_size):
        self.images, self.genres = images, genres
        self.batch_size = batch_size

    def __len__(self):
        return int(np.ceil(len(self.images) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_x = self.images[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.genres[idx * self.batch_size:(idx + 1) * self.batch_size]
        
        return np.array([resize(imread(image), (300, 300)) for image in batch_x]), np.array(batch_y)

def get_train_test():

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
    
    rootDir = './TrainingSpectrograms/'
    for k, v in ClassDict.items():
        for currentDir, subdirList, fileList in os.walk(rootDir+k):
            for png in fileList:
                x_train.append(currentDir+'/'+png)
                y_train.append(v)

    train_x, test_x, train_y, test_y = train_test_split(np.array(x_train), to_categorical(np.array(y_train)), random_state=42)
    return train_x, test_x, train_y, test_y

def create_model(train_x, test_x, train_y, test_y):
    BatchSize = 30
    Epochs = 100
    TrainingGenerator = DataGenerator(train_x, train_y, BatchSize)
    ValidationGenerator = DataGenerator(test_x, test_y, BatchSize)

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3,3), strides=(1,1), activation='relu', input_shape=(300,300, 4)))
    model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)))
    model.add(Conv2D(64, kernel_size=(3,3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(8, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit_generator(generator=TrainingGenerator, steps_per_epoch = int(len(train_x)//BatchSize), epochs=Epochs, verbose=1, validation_data=ValidationGenerator, validation_steps=int(len(test_x)//BatchSize), use_multiprocessing=True, workers=2, max_queue_size=32)

    model_json = model.to_json()
    with open('model.json', 'w') as json_file:
        json_file.write(model_json)
    model.save_weights('model.h5')

    print(model.predict(test_x[:4]))

    print(test_y[:4])

train_x, test_x, train_y, test_y = get_train_test()
create_model(train_x, test_x, train_y, test_y)
