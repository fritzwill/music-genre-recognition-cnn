import os
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
    print(len(line))
    genreList = line[42].strip('[]').split(',')
    genreList = [x.strip() for x in genreList]
    trackDictionary[line[0]] = genreList

mp3Root = '/home/group/ai-fa18-project/fma_small'
exampleNumber = 0
for CurrentDir, DirList, Files in os.walk(mp3Root):
  for song in Files:
    if song[-1] != '3': continue
    songID = song.strip('0')
    songID = songID[:-4]
    print(CurrentDir)
    print('Song file: >{}< ~ SongID: >{}<'.format(song, songID))
    exampleNumber += 1

print('Songs found: {}'.format(exampleNumber))

for k, v in genreDictionary.items():
  print('Genre ID: >{}< Genre: >{}<'.format(k, v))

for k, v in trackDictionary.items():
  print('Track ID: >{}< Genres: >{}<'.format(k, v))
