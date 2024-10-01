# Version 1.0
# author: Patrick Scholz Contact: patrick.alexander.scholz@rwth-aachen.de
# currently intended to work for up to 99 simultaneously measured channels, files must be in *.tif format
# Image file name format: SeriesXXX_tYYY_z0_chZZ with XXX as increment of the run per day, YYY as timeframe and ZZ as Channel number
# for now the only hard requirement for the name format is the name ends with chZZ.tif

#import modules
import numpy as np
import matplotlib.pyplot as plt
import cv2

#coordinates of upper left corner and lower right corner of the catalyst rectangle
x = 0
x1 = 0
y = 0
y1 = 0

def getArea(image, cutoffB, cutoffG, cutoffR, color_rangelower = 50, color_rangeupper = 250):
    image = cv2.imread("test.png")
    print(image.shape)
    # Define the target color and color range (in RGB format)
    target_color = (cutoffB, cutoffG, cutoffR)  # OpenCV order of colors is BGR
    # Calculate the percentage of the image that is within the color range of the target
    lower_bound = np.clip(np.array(target_color) - color_rangelower, 0, 255)
    upper_bound = np.clip(np.array(target_color) + color_rangeupper, 0, 255)
    mask = cv2.inRange(image, lower_bound, upper_bound)
    cv2.imwrite('mask2.png', mask)  # Save mask for testing
    num_pixels = image.shape[0] * image.shape[1]
    print("Pixelnumber: " + str(num_pixels))
    print(image.shape[0], image.shape[1])
    target_pixels = cv2.countNonZero(mask)
    print(mask)
    print(target_pixels)
    percentage = (target_pixels / num_pixels) * 100

    return percentage

def showImagesFromStack(stack, framerate, defaultFrame = 0):
    cols = int(stack.shape[0]/framerate)
    fig, axes = plt.subplots(nrows=1, ncols=cols, dpi=5000)
    if cols >> 1:
        for i in range(cols):
            im = stack[i*framerate]
            axes[i].imshow(im)
            axes[i].axis('off')
    else:
        im = stack[defaultFrame]
        axes.imshow(im)
        axes.axis('off')
    plt.show()
    #fig.savefig('test.png')

def substractDust(stack):
    dust = stack[0]
    dust[dust < 250] = 0
    subStack = np.subtract(stack, dust)

    return subStack

def setCatalystBoundrys(xl, xr, yu, yl):            #xl = left x, xr = right x, yu = upper y, yl = lower y
    global x, y, x1, y1
    x = int(xl)
    y = int(yu)
    x1 = int(xr)
    y1 = int(yl)
    print(x, y)


def crop(image):
    croped_image = image[x:x1, y:y1]
    showImagesFromStack(croped_image, 1, 0)