# Version 1.0
# author: Patrick Scholz Contact: patrick.alexander.scholz@rwth-aachen.de

# import needed modules
import imageio
import numpy as np
import promptlib

# read image files
# Image file name format: SeriesXXX_tYYY_z0_ch0Z with XXX as increment of the run per day, YYY as timeframe and Z as Channel number 0 being fluorescent and 1 being optical

prompter = promptlib.Files()
imgFolderPath = prompter.dir()

im1 = imageio.imread(imgFolderPath + '\Series013_t000_z0_ch00.tif')

ImgStack = np.stack((im1), axis=0)
print('Volume dimensions:', ImgStack.shape)