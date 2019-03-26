from keras.models import Sequential, model_from_json
from keras.layers import Dense, Conv2D, Flatten
from dataTools import getDataset
from songToData import createSlicesFromAudio
import argparse
from config import batchSize
from config import filesPerGenre
from config import genres
from config import validationRatio, testRatio
from config import sliceSize
import json

# create CNN
def create_model(train_x, test_x, train_y, test_y):
    model = Sequential()
    model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(128,128, 1)))

    model.add(Conv2D(32, kernel_size=3, activation='relu'))
    model.add(Flatten())
    model.add(Dense(8, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=3, batch_size=batchSize)

    scores = model.evaluate(test_x, test_y, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    # saving model
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model.h5")
    print("Saved model to disk")

# train model more and save weights and model
def train_more(train_x, test_x, train_y, test_y):
    with open('model.json') as f:
        data = json.load(f)
        json_string = json.dumps(data)
    model = model_from_json(json_string)
    model.load_weights('model.h5')
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=4, batch_size=batchSize)
    scores = model.evaluate(test_x, test_y, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model.h5")

if __name__ == "__main__":

    # argparser for mode
    parser = argparse.ArgumentParser(description="slice or no")
    parser.add_argument('-m', dest='mode', type=str, default='train')
    args = parser.parse_args()

    # if you want to slice, create them from the mp3 files
    if args.mode == 'slice':
        createSlicesFromAudio()
    elif args.mode == 'train':

        # if you are training, return the training and testing datasets
        train_x, train_y, test_x, test_y = getDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode=args.mode)
        create_model(train_x, test_x, train_y, test_y)
    elif args.mode == 'more':

        # want to train it more but not create new CNN
        train_x, train_y, test_x, test_y = getDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode=args.mode)
        train_more(train_x, test_x, train_y, test_y)
    elif args.mode == 'test':
        test_X, test_Y = getDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="test")
        with open('model.json') as f:
            data = json.load(f)
            json_string = json.dumps(data)
        model = model_from_json(json_string)
        model.load_weights('model.h5')
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        score, testAccuracy = model.evaluate(test_X, test_Y)
        print("Score: {}\nTest accuracy: {} ".format(score, testAccuracy))





