from PIL import Image
import os.path

from config import spectrogramsPath, slicesPath

ClassDict = {'Pop': 0,
             'Instrumental': 1,
             'Hip-Hop': 2,
             'Experimental': 3,
             'Electronic': 4,
             'Folk': 5,
             'Rock': 6,
             'International': 7}

#Slices all spectrograms
def createSlicesFromSpectrograms(desiredSize):
    for k, v in ClassDict.items():
        for currentDir, subdirList, fileList in os.walk(spectrogramsPath+k):
            for filename in fileList:
                sliceSpectrogram(filename,desiredSize, k)

#Creates slices from spectrogram
def sliceSpectrogram(filename, desiredSize, genre):

    # Load the full spectrogram
    img = Image.open(spectrogramsPath+genre+'/'+filename)

    #Compute approximate number of 128x128 samples
    width, height = img.size
    nbSamples = int(width/desiredSize)
    width - desiredSize

    #Create path if not existing
    print("About to create Slices for file {}".format(nbSamples))
    #For each sample
    for i in range(10):
        print("Creating slice: ", (i+1), "/", nbSamples, "for", genre, filename)
        #Extract and save 128x128 sample
        startPixel = i*desiredSize
        imgTmp = img.crop((startPixel, 1, startPixel + desiredSize, desiredSize + 1))
        imgTmp.save(slicesPath+"{}/{}_{}".format(genre, i, filename))
