import vtk
import os
import imageio as iio
import numpy as np
import matplotlib.pyplot as plt
import itk
import napari
from skimage import color
import re
import stacking

voxelDim = {}
shapeDim = {}

aspect_xz = 1
aspect_yz = 1
def imageStackerPerChannel(path, channel):
    imageList= []
    # 3Dimagearray has the shape (No. of frames in 3D, No. of frames in 2D, X, Y, Color)
    arrayOfThreeDim = np.zeros((shapeDim.get("T"), shapeDim.get("Z"), shapeDim.get("Y"), shapeDim.get("X"), 3))
    channelByTime = [[] for i in range(shapeDim.get("T"))]

    for imagepath in channel:
        matchTime = re.search(r't(\d+)', imagepath)
        channelByTime[int(matchTime.group(1))].append(imagepath)

    for timestamp in range(len(channelByTime)):
        if channelByTime[timestamp] != []:
            for imagepath in channelByTime[timestamp]:
                imageList.append(itkImaging(iio.v3.imread(path + imagepath)))
            arrayOfThreeDim[timestamp] = np.stack(imageList)
        imageList = []

    return arrayOfThreeDim

def showXYZprojection(image):
    max_z = np.max(image, axis = 0)
    plt.imshow(max_z)
    plt.show()

    max_y = np.max(image, axis = 1)
    plt.imshow(max_y, aspect=aspect_xz)
    plt.show()

    max_x = np.max(image, axis = 2)
    plt.imshow(max_x, aspect=aspect_yz)
    plt.show()

def itkImaging(image):
    itkImage = itk.image_view_from_array(image)
    itkImage.SetSpacing(np.double([voxelDim.get("X"), voxelDim.get("Y"), voxelDim.get("Z")]))
    return itkImage


if __name__ == "__main__":
    image_folder = "C:\\Users\\schol\\Documents\\AVT\\04_Experimentals\\20240903-pasc10\\Series005"
    channels = [[] for i in range(stacking.getNumberOfChannels(image_folder))]
    channels = stacking.sortFilenames(image_folder, channels)

    shapeDim = {"X" : 1024, "Y" : 512, "Z" : 14, "T" : 45}
    voxelDim = {"X" : 0.355, "Y" : 0.355, "Z" : 2.588, "T" : 9.583}

    aspect_xz = voxelDim.get("Z") / voxelDim.get("X")
    aspect_yz = voxelDim.get("Z") / voxelDim.get("Y")

    stack = imageStackerPerChannel(image_folder, channels[0])
    graystack = color.rgb2gray(stack)

    viewer = napari.Viewer()

    viewer.add_image(graystack)
    napari.run()
