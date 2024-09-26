# Version 1.0
# author: Patrick Scholz Contact: patrick.alexander.scholz@rwth-aachen.de
#currently intended to work for up to 10 simultaneously measured channels

# import needed modules
import imageio as iio
import numpy as np
import promptlib
import os

# read image files
# Image file name format: SeriesXXX_tYYY_z0_ch0Z with XXX as increment of the run per day, YYY as timeframe and Z as Channel number

#create list into which the image get sorted by channel
channels = [[] for i in range(10)]
#request folder path
prompter = promptlib.Files()
#write path into string
imgFolderPath = prompter.dir()
#create directory object
imgDirectory = os.fspath(imgFolderPath)

def sort (channelnumber, imagename):
    path = "\\" + imagename
    channels[channelnumber].append(path)

for file in os.listdir(imgDirectory):
    filename = os.fsdecode(file)
    #sorting images into their channels
    match filename[-5]:
        case "0":
            sort(0, filename)
        case "1":
            sort(1, filename)
        case "2":
            sort(2, filename)
        case "3":
            sort(3, filename)
        case "4":
            sort(4, filename)
        case "5":
            sort(5, filename)
        case "6":
            sort(6, filename)
        case "7":
            sort(7, filename)
        case "8":
            sort(8, filename)
        case "9":
            sort(9, filename)


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