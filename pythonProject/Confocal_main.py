# Version 1.0
# author: Patrick Scholz Contact: patrick.alexander.scholz@rwth-aachen.de
# currently intended to work for up to 99 simultaneously measured channels
# Image file name format: SeriesXXX_tYYY_z0_chZZ with XXX as increment of the run per day, YYY as timeframe and ZZ as Channel number

# import needed modules
import imageio as iio
import numpy as np
import promptlib
import os

def sort (imagename):
    if imagename.endswith(".tif"):
        channelnumber = int(imagename[-6:-4])
        path = "\\" + imagename
        channels[channelnumber].append(path)

def getNumberOfChannels(imgDirectory):
    numberOfChannels = []
    for file in os.listdir(imgDirectory):
        filename = os.fsdecode(file)
        filenameEnding = filename[-6:]
        if filenameEnding in numberOfChannels:
            break
        else:
            if filenameEnding.endswith(".tif"):
                numberOfChannels.append(filenameEnding)
    return len(numberOfChannels)

# read image files

#request folder path
prompter = promptlib.Files()
#write path into string
imgFolderPath = prompter.dir()
#create directory object
imgDirectory = os.fspath(imgFolderPath)
#create list into which the image get sorted by channel
channels = [[] for i in range(getNumberOfChannels(imgDirectory))]


for file in os.listdir(imgDirectory):
    filename = os.fsdecode(file)
    #sorting images into their channels
    sort(filename)


#imagepaths in list structure
imgPathList=[[] for i in range(len(channels))]
for i in range(len(channels)): #iterating over the channels
    if channels[i] == []: #check if channel is empty
        break
    else:
        for j in range(len(channels[i])): #iterating over the paths in this channel
            imgPath = imgDirectory + channels[i][j]
            imgPathList[i].append(imgPath)

#images into a list structure
imgList = [[] for i in range(len(channels))]
for i in range(len(imgPathList)): #iterating over the channels
    if channels[i] == []: #check if channel is empty
        break
    else:
        for j in range(len(imgPathList[i])): #iterating over the paths per channel
            imgList[i].append(iio.v3.imread(imgPathList[i][j]))


#stacking the images
imgStack = []
for i in range(len(imgList)):
    if channels[i] == []: #check if channel is empty
        break
    else:
        stack = np.stack(imgList[i], axis=0)
        imgStack.append(stack)
print('Volume dimensions:', imgStack[0].shape)
print('Volume dimensions:', imgStack[1].shape)