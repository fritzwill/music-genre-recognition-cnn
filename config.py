import os
#Define paths for files
spectrogramsPath = "tommySpect/"
slicesPath = "slices/"
datasetPath = "data/"
rawDataPath = "Data/Raw/"


#Spectrogram resolution
pixelPerSecond = 50

#Slice parameters
sliceSize = 128

#Dataset parameters
filesPerGenre = 1000
validationRatio = 0.3
testRatio = 0.1

#Model parameters
batchSize = 128
learningRate = 0.001
nbEpoch = 20


genres = os.listdir(slicesPath)
genres = [filename for filename in genres if os.path.isdir(slicesPath+filename)]