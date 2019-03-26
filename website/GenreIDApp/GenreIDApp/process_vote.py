from pydub import AudioSegment
import os, sys
import wave
import pylab
import csv
import random  # For simulated confidence
from keras.models import load_model, model_from_json
import json
from PIL import Image
import numpy as np
from itertools import islice

MAIN_FOLDER = "/tmp/processing"
WAVS_FOLDER = "/tmp/processing/wavs"
MP3S_FOLDER = "/tmp/processing/mp3s"
MP3S_FOLDER = "/tmp/processing/mp3s"
STATIC_PROCESSING_FOLDER = "/var/www/GenreIDApp/GenreIDApp/static/processing"
SPECTROS_FOLDER = "/var/www/GenreIDApp/GenreIDApp/static/processing/spectros"
MODEL_JSON = "/var/www/GenreIDApp/GenreIDApp/static/processing/model/model.json"
MODEL_H5 = "/var/www/GenreIDApp/GenreIDApp/static/processing/model/model.h5"

NUM_SAMPLES = 20
IMG_SIZE = 128

GENRE_IDS = {
    0: "Pop",
    1: "Instrumental",
    2: "Hip-Hop",
    3: "Experimental",
    4: "Electronic",
    5: "Folk",
    6: "Rock",
    7: "International"
}


def load_and_resize_image(filename, image_size):
    img = Image.open(filename).convert('L')
    img = img.resize((image_size, image_size), resample=Image.ANTIALIAS)
    image_data = np.asarray(img, dtype=np.uint8).reshape(1, image_size,image_size,1)
    image_data = image_data/255.
    return image_data


def get_wav_info(wav_file_path):
    wav = wave.open(wav_file_path, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'Int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate


def make_spectros(wav_base_file_path):
    base_name = os.path.basename(wav_base_file_path)
    spectro_base_path = os.path.join(SPECTROS_FOLDER, "{}".format(base_name))

    for idx in range(NUM_SAMPLES):
        sound_info, frame_rate = get_wav_info(wav_base_file_path + "-{}.wav".format(idx))
        pylab.style.use('grayscale')
        fig, ax = pylab.subplots(1, num=None, figsize=(1,1), dpi=128)
        fig.subplots_adjust(left=0, right=1, bottom=0,top=1)
        pylab.axis('off')
        pylab.specgram(sound_info, Fs=frame_rate)
        pylab.savefig(spectro_base_path + "-{}.png".format(idx))
        pylab.close()

    return spectro_base_path


def predict_genre(spectro_base_path):
    # Load model.
    with open(MODEL_JSON) as f:
        data = json.load(f)
        json_string = json.dumps(data)

    model = model_from_json(json_string)
    model.load_weights(MODEL_H5)

    collect = np.zeros(8)

    # Load spectrograms.
    for idx in range(NUM_SAMPLES):
        spectro_path = spectro_base_path + "-{}.png".format(idx)
        spectro_data = load_and_resize_image(spectro_path, IMG_SIZE)
        result = model.predict(spectro_data)
        collect = np.add(collect, result[0])

    genre = GENRE_IDS[collect.argmax()]
    confidence = collect.max() / NUM_SAMPLES
    return genre, confidence


def process_mp3(mp3_file_path):
    base_name = os.path.basename(mp3_file_path)

    for dir_ in [MAIN_FOLDER, STATIC_PROCESSING_FOLDER, SPECTROS_FOLDER, WAVS_FOLDER, MP3S_FOLDER]:
        try:
            os.mkdir(dir_)
        except FileExistsError:
            continue

    mp3_obj = AudioSegment.from_mp3(mp3_file_path)
    segmented_mp3_arr = mp3_obj[::3000] # Makes slices.

    wav_base_file_path = os.path.join(WAVS_FOLDER, "{}".format(base_name[:-4]))

    for idx, mp3_segment in enumerate(islice(segmented_mp3_arr, NUM_SAMPLES)):
        wav_file_path = wav_base_file_path + "-{}.wav".format(idx)
        mp3_segment.export(wav_file_path, format='wav')

    spectro_base_path = make_spectros(wav_base_file_path)
    spectro_path = spectro_base_path + "-10.png"
    genre, confidence = predict_genre(spectro_base_path)
    return genre, spectro_path, confidence

if __name__ == '__main__':
    mp3_file_path = sys.argv[1]
    genre, spectro_path, confidence = process_mp3(mp3_file_path)

    print(genre, spectro_path, confidence)
