import vtk
import os
import imageio as iio
import numpy as np
import matplotlib.pyplot as plt
import itk
import napari
from skimage import color

voxel_size_x = 0.355
voxel_size_y = 0.355
voxel_size_z = 2.588
voxel_size_t = 9.583

aspect_xz = voxel_size_z/voxel_size_x
aspect_yz = voxel_size_z/voxel_size_y

def imageStacker(image_folder):
    pathlist = []
    imageList= []

    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith('.tif') or filename.endswith('.tiff'):  # Handle both .tif and .tiff
            img_path = os.path.join(image_folder, filename)
            pathlist.append(img_path)
    for i in range(len(pathlist)):
        imageList.append(iio.imread(pathlist[i]))

    imageStack = np.stack(imageList)
    return imageStack

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
    itkImage.SetSpacing(np.double([voxel_size_x, voxel_size_y, voxel_size_z]))
    return itkImage


if __name__ == "__main__":
    image_folder = "C:\\Users\\schol\\Documents\\GitRepos\\Confocal\\Confocal\\pythonProject\\images"
    stack = imageStacker(image_folder)
    graystack = color.rgb2gray(stack)
    print(graystack.shape)
    viewer = napari.Viewer()

    viewer.add_image(itkImaging(graystack))
    napari.run()
