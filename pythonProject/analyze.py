# Version 1.0
# author: Patrick Scholz Contact: patrick.alexander.scholz@rwth-aachen.de
# currently intended to work for up to 99 simultaneously measured channels, files must be in *.tif format
# Image file name format: SeriesXXX_tYYY_z0_chZZ with XXX as increment of the run per day, YYY as timeframe and ZZ as Channel number
# for now the only hard requirement for the name format is the name ends with chZZ.tif

#import modules
import numpy as np
import matplotlib.pyplot as plt


def getArea():
    area = 0

    return area

def showImagesFromStack(stack, framerate, defaultFrame = 0):
    cols = int(stack.shape[0]/framerate)
    fig, axes = plt.subplots(nrows=1, ncols=cols, dpi=1500)
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

def substractDust(stack):
    dust = stack[0]
    dust[dust < 250] = 0
    subStack = np.subtract(stack, dust)

    return subStack
