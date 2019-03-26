import errno
import csv
from subprocess import Popen, PIPE, STDOUT
import os
import eyed3
from slice import createSlicesFromSpectrograms
from config import rawDataPath
from config import spectrogramsPath
from config import pixelPerSecond

#Tweakable parameters
desiredSize = 128

#Define
currentPath = os.path.dirname(os.path.realpath(__file__))

#Remove logs
eyed3.log.setLevel("ERROR")

# raw data : mp3 files on my local machine
rawDataPath = '/Users/tommy/Downloads/fma_small/'

# path to store spectrograms
spectrogramsPath = 'tommySpect/'

# meta data
trackRoot = './fma_metadata/tracks.csv'
genreRoot = './fma_metadata/genres.csv'
ClassDict = {'Pop': 0,
                'Instrumental': 1,
                'Hip-Hop': 2,
                'Experimental': 3,
                'Electronic': 4,
                'Folk': 5,
                'Rock': 6,
                'International': 7}

# create dicts of genre and tracks from meta data
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


#Remove logs
eyed3.log.setLevel("ERROR")

# return whether an image is mono
def isMono(filename):
	audiofile = eyed3.load(filename)
	return audiofile.info.mode == 'Mono'


#Create spectrogram from mp3 files
def createSpectrogram(filename,newFilename, genre, dir):
	# if no directory for genre, create one
	if not os.path.exists(os.path.dirname(spectrogramsPath+genreDictionary[genre]+'/')):
		try:
			os.makedirs(os.path.dirname(spectrogramsPath+genreDictionary[genre]+'/'))
		except OSError as exc:  # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise


	#Create temporary mono track if needed
	if isMono('{}/{}'.format(rawDataPath+dir, filename)):
		command = "cp '{}/{}' '/tmp/{}'".format(rawDataPath+dir, filename,newFilename)
	else:
		command = "sox '{}/{}' '/tmp/{}' remix 1,2".format(rawDataPath+dir, filename,newFilename)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print (errors)

	#Create spectrogram
	command = "sox '/tmp/{}' -n spectrogram -Y 200 -X {} -m -r -o '{}/{}.png'".format(newFilename,pixelPerSecond,spectrogramsPath+genreDictionary[genre], filename[:-4])
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print (errors)

	#Remove tmp mono track
	try:
		os.remove("/tmp/{}".format(newFilename))
	except:
		print("file not removed: /tmp/{}".format(newFilename))

#Creates .png whole spectrograms from mp3 files
def createSpectrogramsFromAudio():

	for CurrentDir, DirList, Files in os.walk(rawDataPath):
		for i, song in enumerate(Files):
			if song.endswith('.mp3'):
				songID = song.strip('0')
				songID = songID[:-4]
				genres = trackDictionary[songID]
				for genre in genres:
					if genreDictionary[genre] not in ClassDict.keys():
						continue
					print("Creating spectrogram for file {}/{}...".format(genre, song))
					createSpectrogram(song, song, genre, CurrentDir.split('/')[-1])



#Whole pipeline .mp3 -> .png slices
def createSlicesFromAudio():
	print ("Creating spectrograms...")
	createSpectrogramsFromAudio()
	print("Spectrograms created!")

	print ("Creating slices...")
	createSlicesFromSpectrograms(desiredSize)
	print("Slices created!")