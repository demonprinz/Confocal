# Version 1.0
# author: Patrick Scholz Contact: patrick.alexander.scholz@rwth-aachen.de
#currently intended to work for up to 10 simultaneously measured channels

# import needed modules
import imageio as iio
import numpy as np
import promptlib
import os

# read image files
# Image file name format: SeriesXXX_tYYY_z0_ch0Z with XXX as increment of the run per day, YYY as timeframe and Z as Channel number 0 being fluorescent and 1 being optical

#create list into which the image get sorted by channel
channels = [[] for i in range(10)]
print(channels)
#request folder path
prompter = promptlib.Files()
#write path into string
imgFolderPath = prompter.dir()
#create directory object
imgDirectory = os.fspath(imgFolderPath)

def sort (channelnumber, imagename):
    channels[channelnumber].append(imagename)

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

print(channels)

for i in range length(channels[1]):
    print(channels[1][i])
#imagepath tuple
# tup=()
# for i in channels [1]:
#     imgFolderPath = imgDirectory + "/"
#     tup = tup + (imgFolderPath + [channels[1][i])
# print(tup)
#im1 = iio.v3.imread(imgFolderPath + r'\Series013_t000_z0_ch00.tif') #r prefix to protect the Backslash needed for the path

#ImgStack = np.stack((iio.v3.imread(imgFolderPath + channels[0])), axis=0)
#print('Volume dimensions:', ImgStack.shape)