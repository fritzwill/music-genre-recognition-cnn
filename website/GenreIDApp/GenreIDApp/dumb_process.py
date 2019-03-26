from pydub import AudioSegment
import os, sys
import wave
import pylab
import csv

MAIN_FOLDER = "/tmp/processing"
# SPECTROS_FOLDER = "/tmp/processing/spectros"
WAVS_FOLDER = "/tmp/processing/wavs"
MP3S_FOLDER = "/tmp/processing/mp3s"
STATIC_PROCESSING_FOLDER = "/var/www/GenreIDApp/GenreIDApp/static/processing"
SPECTROS_FOLDER = "/var/www/GenreIDApp/GenreIDApp/static/processing/spectros"


def get_wav_info(wav_file_path):
    wav = wave.open(wav_file_path, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'Int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate


def make_spectro(wav_file_path):
    base_name = os.path.basename(wav_file_path)
    spectro_path = os.path.join(SPECTROS_FOLDER, "{}.png".format(base_name[:-4]))
    sound_info, frame_rate = get_wav_info(wav_file_path)

    pylab.figure(num=None, figsize=(19,12))
    pylab.subplot(111)
    # pylab.title('spectrogram of %r' % sample)
    pylab.specgram(sound_info, Fs=frame_rate)
    pylab.savefig(spectro_path)
    pylab.close()

    return spectro_path


def predict_genre(wav_file_path):
    return "Neo-Rap Country"


def process_mp3(mp3_file_path):
    base_name = os.path.basename(mp3_file_path)

    for dir_ in [MAIN_FOLDER, STATIC_PROCESSING_FOLDER, SPECTROS_FOLDER, WAVS_FOLDER, MP3S_FOLDER]:
        try:
            os.mkdir(dir_)
        except FileExistsError:
            continue

    mp3_obj = AudioSegment.from_mp3(mp3_file_path)
    segmented_mp3_arr = list(mp3_obj[::3000]) # Makes slices.

    wav_file_path = os.path.join(WAVS_FOLDER, "{}-0.wav".format(base_name[:-4]))
    segmented_mp3_arr[0].export(wav_file_path, format='wav')

    spectro_path = make_spectro(wav_file_path)
    genre = predict_genre(wav_file_path)
    return genre, spectro_path

if __name__ == '__main__':
    mp3_file_path = sys.argv[1]
    genre, spectro_path = process_mp3(mp3_file_path)
    print(genre, spectro_path)
