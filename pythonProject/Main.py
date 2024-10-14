# Version 1.0
# author: Patrick Scholz Contact: patrick.alexander.scholz@rwth-aachen.de
# currently intended to work for up to 99 simultaneously measured channels, files must be in *.tif format
# Image file name format: SeriesXXX_tYYY_z0_chZZ with XXX as increment of the run per day, YYY as timeframe and ZZ as Channel number
# for now the only hard requirement for the name format is the name ends with chZZ.tif


#getting the needed functions
import stacking
import analyze
import promptlib
import os
import metahandler

# read image files

#request folder path
prompter = promptlib.Files()

#write path into string
imgFolderPath = prompter.dir()

#create directory object
imgDirectory = os.fspath(imgFolderPath)

#get frametime
analyze.frametime = metahandler.getFrameTime(imgFolderPath)

#get echemdata
promter2 = promptlib.Files()
echemDataPath = promter2.file()

echemData = metahandler.getElectricData(echemDataPath)
analyze.timeDiff = metahandler.getTimeDifference(imgFolderPath, echemDataPath)


#create list into which the image get sorted by channel
channels = [[] for i in range(stacking.getNumberOfChannels(imgDirectory))]


#sorting images into the channels List
channels = stacking.sortFilenames(imgDirectory, channels)

#images into a list structure
imgList = stacking.imageLists(stacking.imagePaths(channels, imgDirectory))

#stacking the images
imgStack = stacking.stackingImages(imgList)

subStack = analyze.substractDust(imgStack)
#get stacked images of the catalyst area only

cropped_stack= analyze.cropper(subStack[0][int(len(subStack[0])/2)], subStack)
# print(analyze.getArea(cropped_stack[0][140], 0,130,0))
analyze.showImagesFromStack(cropped_stack[0], 100, 140)

analyze.outputWithEchem(cropped_stack[0], cutoffG=140, color_rangelower= 60, echemData = echemData)

