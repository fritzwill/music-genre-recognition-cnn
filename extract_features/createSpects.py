from pydub import AudioSegment
import os
import wave
import pylab
import csv

trackRoot = '/home/group/ai-fa18-project/fma_metadata/tracks.csv'
genreRoot = '/home/group/ai-fa18-project/fma_metadata/genres.csv'

genreDictionary = dict()
with open(genreRoot) as genreFile:
  for line in genreFile:
    line = line.split(',')
    genreDictionary[line[0]] = line[3].replace(' ', '_')

trackDictionary = dict()
with open(trackRoot) as trackFile:
  csv_reader = csv.reader(trackFile, delimiter=',')
  for line in csv_reader:
    genreList = line[42].strip('[]').split(',')
    genreList = [x.strip() for x in genreList]
    trackDictionary[line[0]] = genreList

def getSampleInfo(sample):
  wav = wave.open(sample, 'r')
  frames = wav.readframes(-1)
  soundInfo = pylab.fromstring(frames, 'Int16')
  frameRate = wav.getframerate()
  wav.close()
  return soundInfo, frameRate

def createSpectorgram(sample, genres, sampleNum):
  soundInfo, frameRate = getSampleInfo(sample)
  pylab.figure(num=None, figsize=(19,12))
  pylab.subplot(111)
  pylab.title('spectrogram of %r' % sample)
  pylab.specgram(soundInfo, Fs=frameRate)
  for genre in genres:
    pylab.savefig('../spectrograms/{}/{}.png'.format(genreDictionary[genre], sampleNum))
  print('Saved image {}...'.format(sampleNum))
  pylab.close()


mp3Root = '/home/group/ai-fa18-project/fma_small'
exampleNumber = 1
for CurrentDir, DirList, Files in os.walk(mp3Root):
  for song in Files:
    if song[-1] != '3': continue
    songID = song.strip('0')
    songID = songID[:-4]
    songPath = CurrentDir + '/' + song
    genres = trackDictionary[songID]
    mp3 = AudioSegment.from_mp3(songPath)
    segmentedMp3 = mp3[::3000]
    for i, segment in enumerate(segmentedMp3):
      sample = '../wav_files/' + songID + '-{}.wav'.format(i)
      segment.export(sample, format='wav')
      createSpectorgram(sample, genres, exampleNumber)
      exampleNumber += 1
