# Version 1.0
# author: Patrick Scholz Contact: patrick.alexander.scholz@rwth-aachen.de
# currently intended to work for up to 99 simultaneously measured channels, files must be in *.tif format
# Image file name format: SeriesXXX_tYYY_z0_chZZ with XXX as increment of the run per day, YYY as timeframe and ZZ as Channel number
# for now the only hard requirement for the name format is the name ends with chZZ.tif

#import modules
import numpy as np
import matplotlib.pyplot as plt
import cv2
import tkinter as tk

from matplotlib import cm

# Global variables to store the coordinates
start_point = None
end_point = None
drawing = False
image = None
imageStack = None
cropped_stack = None
index = 0
voxelDim = None
timeDiff = 0
path = ""


def getArea(image, cutoffB, cutoffG, cutoffR, color_rangelower = 45, color_rangeupper = 250):
    #image = cv2.imread("test.png")
    global index
    # Define the target color and color range
    target_color = (cutoffB, cutoffG, cutoffR)  # OpenCV order of colors is BGR
    # Calculate the percentage of the image that is within the color range of the target
    lower_bound = np.clip(np.array(target_color) - color_rangelower, 0, 255)
    upper_bound = np.clip(np.array(target_color) + color_rangeupper, 0, 255)
    mask = cv2.inRange(image, lower_bound, upper_bound)

    cv2.imwrite(path + '\\masks\\mask' + str(index) + '.png', mask)  # Save mask for testing
    index += 1
    num_pixels = image.shape[0] * image.shape[1]

    target_pixels = cv2.countNonZero(mask)

    percentage = (target_pixels / num_pixels) * 100

    return percentage

def showImagesFromStack(stack, framerate, defaultFrame = 0):
    cols = int(stack.shape[0]/framerate)
    fig, axes = plt.subplots(nrows=1, ncols=cols, dpi=500)
    if cols >> 1:
        for i in range(cols):
            im = stack[1 + i*framerate]
            axes[i].imshow(im)
            axes[i].axis('off')
    else:
        im = stack[defaultFrame]
        axes.imshow(im)
        axes.axis('off')
    plt.show()
    #fig.savefig('test.png')

def substractDust(stack):
    subStack = [[] for i in range(len(stack))]
    for i in range(len(stack)):
        dust = stack[i][0]
        dust[dust < 250] = 0
        subtracted = np.subtract(stack[i], dust)
        subStack[i] = subtracted

    return subStack


def crop(x, x1, y, y1):
    global cropped_stack
    for i in range(len(cropped_stack)):
        cropped_stack[i] = imageStack[i][:,y:y1, x:x1]


# Mouse callback function
def draw_rectangle(event, x, y, flags, param):

    global start_point, end_point, drawing, image
    # When the left mouse button is pressed, record the starting point
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
        end_point = start_point

    # When the mouse is moved while the left button is pressed, update the endpoint
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end_point = (x, y)

    # When the left mouse button is released, finalize the rectangle
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)

        # Draw the rectangle on the image
        cv2.rectangle(image, start_point, end_point, (200, 0, 0), 1)
        cv2.imshow("Image Cropper", image)
        point1 = list(start_point)
        point2 = list(end_point)
        if point1[1] > point2[1]:

            value = point1[1]
            point1 = [point1[0], point2[1]]
            point2 = [point2[0], value]
            start_point = tuple(point1)
            end_point = tuple(point2)

        if start_point[0] > end_point[0]:
            value = point1[0]
            point1 = [point2[0], point1[1]]
            point2 = [value, point2[1]]
            start_point = tuple(point1)
            end_point = tuple(point2)

        crop(start_point[0], end_point[0], start_point[1], end_point[1])

def cropper(img, imgStack):
    # Create a window and set the mouse callback
    global image, imageStack, cropped_stack
    cv2.namedWindow("Image Cropper")
    image = img
    imageStack = imgStack
    cropped_stack = [[] for i in range(len(imgStack))]
    cv2.setMouseCallback("Image Cropper", draw_rectangle)

    while True:
        cv2.imshow("Image Cropper", image)
        key = cv2.waitKey(1)

        # Break the loop when 'q' is pressed
        if key == ord('q'):
            break

    # Cleanup
    cv2.destroyAllWindows()
    return cropped_stack

def areaList(imageStack, cutoffB, cutoffG, cutoffR, color_rangelower = 45, color_rangeupper = 250, quenching = False):
    global index
    areaList = []
    for i in range(imageStack.shape[0]):
        if quenching:
            areaList.append(1-(getArea(imageStack[i], cutoffB, cutoffG, cutoffR, color_rangelower, color_rangeupper)))
        else:
            areaList.append(getArea(imageStack[i], cutoffB, cutoffG, cutoffR, color_rangelower, color_rangeupper))
    index = 0
    return areaList

def output(imageStack, cutoffB = 0, cutoffG = 130, cutoffR = 0, color_rangelower = 45, color_rangeupper = 250):
    xValues = [voxelDim.get("T") * i for i in range(imageStack.shape[0])]
    areaValues = areaList(imageStack, cutoffB, cutoffG, cutoffR, color_rangelower, color_rangeupper)
    plt.plot(xValues, areaValues)
    plt.xticks(np.arange(0, len(areaValues)*voxelDim.get("T"), 30))
    plt.xlim(0, len(areaValues)*voxelDim.get("T")+1)
    plt.xlabel('time [s]')
    plt.ylabel('active area [%]')
    plt.title("Active area over time")
    plt.show()


def outputWithEchem(imageStack, cutoffB=0, cutoffG=130, cutoffR=0, color_rangelower=45, color_rangeupper=250, echemData=None):
    xValuesImageStack = [voxelDim.get("T") * i for i in range(imageStack.shape[0])]
    areaValues = areaList(imageStack, cutoffB, cutoffG, cutoffR, color_rangelower, color_rangeupper)
    if echemData is not None:
        ydata = []
        xdata = [int(i)+timeDiff for i in echemData[2][2:]]
        match echemData[0]:
            case "GALVANOSTATIC":
                for i in echemData[3][2:]:
                    ydata.append(float(i.replace(',', '.')))

                    label = "Voltage [V vs V ref]"
            case "POTENTIOSTATIC":
                for i in echemData[4][2:]:
                    ydata.append(float(i.replace(',', '.'))*1000000)
                    label = "Current ["+ r'$\mu$' +"A]"

    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('time [s]', labelpad=5)
    ax1.set_ylabel('active area [%]', color=color)
    ax1.plot(xValuesImageStack, areaValues, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.tick_params(axis = 'x', pad = 10)
    ax1.set_xlim(0, len(areaValues)*voxelDim.get("T")+1)
    ax1.set_title("Active area and electrochemical data over time")
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel(label, color=color)
    ax2.plot(xdata, ydata, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()

    plt.show()

    fig.savefig(path + '\\plots\\plotAreaAndEchem.png', bbox_inches='tight')  # Save mask for testing


def userInput():
    master = tk.Tk()
    e = tk.Entry(master)
    e.pack()

    e.focus_set()

    def callback():
        print(e.get())  # This is the text you may want to use later
        master.quit()

    b = tk.Button(master, text="OK", width=10, command=callback)
    b.pack()

    e.mainloop()


def histogram(imageStack, percentile = 0.75):

    histogramColorsList = []
    cutoffs =[]
    # tuple to select colors of each channel line
    colors = ("red", "green", "blue")
    histogram = np.zeros(256, dtype=int)
    # create the histogram value list, with three lists, one for each color
    for channel_id, color in enumerate(colors):
        for i in range(imageStack.shape[0]):
            histogramvalue, bin_edges = np.histogram(
                imageStack[i][:, :, channel_id], bins=256, range=(0, 256)
            )
            histogram += histogramvalue
        histogramColorsList.append(histogram)
        histogram = np.zeros(256, dtype=int)


    for i in range(3):
        value = 0
        for j in range(256):
            if value >= np.sum(histogramColorsList[i])*percentile:
                cutoffs.append(j-1)
                break
            value += histogramColorsList[i][j]

    return cutoffs

def activity(imageStack, cutoffB=0, cutoffG=130, cutoffR=0, color_rangelower=45, color_rangeupper=250, echemData=None):
    #currentdensity per active area is the idea
    areaPercentageValues = areaList(imageStack, cutoffB, cutoffG, cutoffR, color_rangelower, color_rangeupper)
    percentageArray = np.array(areaPercentageValues)
    areaValues = ((percentageArray/100)*(imageStack.shape[2]*voxelDim.get("X")*imageStack.shape[1]*voxelDim.get("Y"))).tolist()

    ydata = []
    xdata = []

    for i in echemData[4][2:]:
        ydata.append(float(i.replace(',', '.')) * 1000000000)
    # for i in echemData[3][2:]:
    #     xdata.append(float(i.replace(',', '.')))

    relevantAreaList = areaValues[int(timeDiff/voxelDim.get("T"))+1:int(len(ydata)+timeDiff/voxelDim.get("T"))]

    if voxelDim.get("T") <= 1:
        xdata = [i for i in range(len(relevantAreaList))]
    else:
        xdata = [i*voxelDim.get("T") for i in range(len(relevantAreaList))]
    currPerArea = [i / j for i, j in zip(ydata, relevantAreaList)]
    plt.plot(xdata, currPerArea)
    plt.xticks(np.arange(0, len(ydata)+1, 30))
    plt.tick_params(axis = "x",  pad = 10)
    plt.xlim(0, len(ydata)+1)
    plt.gca().invert_yaxis()
    plt.xlabel('time [s]')
    plt.ylabel('Current per active area [mA$mm^{-2}$'+"]")
    plt.title("Activity of the catalyst")

    plt.savefig(path + '\\plots\\plotActivity.png', bbox_inches='tight')  # Save mask for testing
    plt.show()

def difArea(imageStackDye1, imageStackDye2, quenchingDye1 = False, quenchingDye2 = False, cutoffB1=0, cutoffG1=130, cutoffR1=0, cutoffB2=130, cutoffG2=0, cutoffR2=0, color_rangelower=45, color_rangeupper=250):
    xValuesImageStack = [voxelDim.get("T") * i for i in range(imageStackDye1.shape[0])]
    areaValuesDye1 = areaList(imageStackDye1, cutoffB1, cutoffG1, cutoffR1, color_rangelower, color_rangeupper, quenchingDye1)
    areaValuesDye2 = areaList(imageStackDye2, cutoffB2, cutoffG2, cutoffR2, color_rangelower, color_rangeupper, quenchingDye2)
    areaDif = [i-j for i,j in zip(areaValuesDye1, areaValuesDye2)]

    plt.plot(xValuesImageStack, areaDif)
    plt.xticks(np.arange(0, len(areaDif) + 1, 30))
    plt.tick_params(axis="x", pad=10)
    plt.xlim(0, len(areaDif) + 1)

    plt.xlabel('time [s]')
    plt.ylabel('Difference in Area between dyes [%]')
    plt.title("Difference in Area between Dyes showing activity and Electrolyte flow")

    plt.savefig(path + '\\plots\\AreaDif.png', bbox_inches='tight')  # Save mask for testing
    plt.show()

def threeDPixellinePlot(imageStack, pixelline = None, pixelwidth = 2 ):
    if pixelline is None or (not isinstance(pixelline, (int, float))):
        line = int(imageStack.shape[2]*(1/3))
    elif isinstance(pixelline, float):
        line = int(imageStack.shape[2]*(pixelline))
    elif isinstance(pixelline, int):
        line = pixelline

    intensitiesOverTime = np.zeros(shape=(imageStack.shape[0]-1, imageStack.shape[1]))
    for imageindex in range(imageStack.shape[0]-1):
        lineIntensities = np.zeros(imageStack.shape[1])
        for i in range(pixelwidth):
            lineIntensities += imageStack[imageindex,:,line+i,1]
        lineIntensities /= pixelwidth
        lineIntensities = np.flip(lineIntensities, axis = 0)
        box = np.ones(int(pixelwidth*(2/3))) / int(pixelwidth*(2/3))
        intensities_smooth = np.convolve(lineIntensities, box, mode='same')
        intensitiesOverTime[imageindex] = intensities_smooth

    x,y = np.meshgrid(np.arange(0, (imageStack.shape[0]-1)), np.arange(0, imageStack.shape[1]))
    intensitiesOverTime = np.transpose(intensitiesOverTime)
    intensitiesOverTime /= np.max(intensitiesOverTime)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    surf = ax.plot_surface(x*voxelDim.get("T"), y*voxelDim.get("Y"), intensitiesOverTime, cmap=cm.inferno)
    ax.set_ylabel('depth ['+ r'$\mu$'+'m]', fontsize=12)
    ax.set_xlabel('time [s]', fontsize=12)
    ax.set_zlabel('Intensity I/$I_{max}$', fontsize=12)
    ax.set_xlim(voxelDim.get("T")*(imageStack.shape[0]-1), 0)
    ax.set_ylim(0, voxelDim.get("X")*(imageStack.shape[1]))
    ax.set_zlim(0, np.max(intensitiesOverTime)+0.02)
    plt.show()

def twoDPixellinePlot(imageStack, pixelline=None, pixelwidth=2):
    if pixelline is None or (not isinstance(pixelline, (int, float))):
        line = int(imageStack.shape[2] * (1 / 3))
    elif isinstance(pixelline, float):
        line = int(imageStack.shape[2] * (pixelline))
    elif isinstance(pixelline, int):
        line = pixelline

    intensitiesOverTime = np.zeros(shape=(imageStack.shape[0] - 1, imageStack.shape[1]))
    for imageindex in range(imageStack.shape[0] - 1):
        lineIntensities = np.zeros(imageStack.shape[1])
        for i in range(pixelwidth):
            lineIntensities += imageStack[imageindex, :, line + i, 1]
        lineIntensities /= pixelwidth
        lineIntensities = np.flip(lineIntensities, axis=0)
        box = np.ones(int(pixelwidth * (2 / 3))) / int(pixelwidth * (2 / 3))
        intensities_smooth = np.convolve(lineIntensities, box, mode='same')
        intensitiesOverTime[imageindex] = intensities_smooth

    intensitiesOverTime = np.transpose(intensitiesOverTime)
    intensitiesOverTime /= np.max(intensitiesOverTime)

    plt.imshow(intensitiesOverTime, extent=[0,imageStack.shape[0]*voxelDim.get("T"),imageStack.shape[1]*voxelDim.get("Y"),0], vmin=0, vmax=1, cmap='inferno')
    cbar = plt.colorbar()
    cbar.set_label('Intensity I/$I_{max}$', size=12)
    plt.gca().invert_yaxis()
    plt.xlabel("Time [s]")
    plt.ylabel(r'Y-Axis coordinate [$\mu$m]')

    plt.show()

