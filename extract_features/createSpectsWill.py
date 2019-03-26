from pydub import AudioSegment
import os
import wave
import pylab
import csv
from subprocess import Popen, PIPE, STDOUT

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

mp3Root = '/home/group/ai-fa18-project/fma_small'
exampleNumber = 1
for CurrentDir, DirList, Files in os.walk(mp3Root):
  for i, song in enumerate(Files):
    if song[-1] != '3': continue
    songID = song.strip('0')
    songID = songID[:-4]
    songPath = CurrentDir + '/' + song
    genres = trackDictionary[songID]
    mp3 = AudioSegment.from_mp3(songPath)
    for genre in genres:
      print("Creating spectogram for file {}/{}".format(i, len(Files)))
      command = "sox '{}' -n spectrogram -Y 200 -X 50 -m -r -o '../willSpect/{}/{}.png'".format(songPath, genreDictionary[genre], songID)
      p = Popen(command, shell=True, stdin=PIPE, stderr=STDOUT, close_fds=True, cwd=os.path.dirname(os.path.realpath(__file__)))
      output, errors = p.communicate()
      if errors:
        print(errors)
