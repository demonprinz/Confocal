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
import cv2
import test

# read image files

#request folder path
prompter = promptlib.Files()

#write path into string
imgFolderPath = prompter.dir()

#create directory object
imgDirectory = os.fspath(imgFolderPath)

#create list into which the image get sorted by channel
channels = [[] for i in range(stacking.getNumberOfChannels(imgDirectory))]

#sorting images into the channels List
channels = stacking.sortFilenames(imgDirectory, channels)

#images into a list structure
imgList = stacking.imageLists(stacking.imagePaths(channels, imgDirectory))

#stacking the images
imgStack = stacking.stackingImages(imgList)


#print(imgStack[0].shape[0])
#analyze.showImagesFromStack(imgStack[0], imgStack[0].shape[0], defaultFrame= 300)
subStack = analyze.substractDust(imgStack[0])
#analyze.showImagesFromStack(subStack, 723, defaultFrame= 140)
#print(analyze.getArea(subStack[140], 0,130,0))

#analyze.crop(subStack[140])

# Create a window and set the mouse callback
cv2.namedWindow("Image")
test.image = subStack[140]
cv2.setMouseCallback("Image", test.draw_rectangle)

while True:
    cv2.imshow("Image", subStack[140])
    key = cv2.waitKey(1)

    # Break the loop when 'q' is pressed
    if key == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()