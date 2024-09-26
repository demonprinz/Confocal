# Version 1.0
# author: Patrick Scholz Contact: patrick.alexander.scholz@rwth-aachen.de
# currently intended to work for up to 99 simultaneously measured channels, files must be in *.tif format
# Image file name format: SeriesXXX_tYYY_z0_chZZ with XXX as increment of the run per day, YYY as timeframe and ZZ as Channel number
# for now the only hard requirement for the name format is the name ends with chZZ.tif

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

def imagePaths(channelList, dir):
    imgPathList = [[] for i in range(len(channelList))]
    for i in range(len(imgPathList)):
        for j in range(len(channelList[i])):
            imgPathList[i].append(dir + channelList[i][j])

    return imgPathList

def imageLists(imgPathList):
    imgLists = [[] for i in range(len(imgPathList))]
    for i in range(len(imgLists)):
        for j in range(len(imgPathList[i])):
            imgLists[i].append(iio.v3.imread(imgPathList[i][j]))

    return imgLists


# for i in range(len(imgList)):
#     if channels[i] == []: #check if channel is empty
#         break
#     else:
#         stack = np.stack(imgList[i], axis=0)
#         imgStack.append(stack)

def stackingImages(imgLists):
    imgStacks = []
    for i in range(len(imgLists)):
        imgStacks.append(np.stack(imgLists[i]))
    return imgStacks



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

#images into a list structure
imgList = imageLists(imagePaths(channels, imgDirectory))

#stacking the images
imgStack = stackingImages(imgList)

print('Volume dimensions:', imgStack[0].shape)
print('Volume dimensions:', imgStack[1].shape)