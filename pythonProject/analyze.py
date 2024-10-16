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

# Global variables to store the coordinates
start_point = None
end_point = None
drawing = False
image = None
imageStack = None
cropped_stack = None
index = 0
frametime = 1
timeDiff = 0



def getArea(image, cutoffB, cutoffG, cutoffR, color_rangelower = 45, color_rangeupper = 250):
    #image = cv2.imread("test.png")
    global index
    # Define the target color and color range
    target_color = (cutoffB, cutoffG, cutoffR)  # OpenCV order of colors is BGR
    # Calculate the percentage of the image that is within the color range of the target
    lower_bound = np.clip(np.array(target_color) - color_rangelower, 0, 255)
    upper_bound = np.clip(np.array(target_color) + color_rangeupper, 0, 255)
    mask = cv2.inRange(image, lower_bound, upper_bound)

    #cv2.imwrite('C:\\Users\\schol\\Documents\\AVT\\04_Experimentals\\20240903-pasc10\\Series003\\masks\\mask' + str(index) + '.png', mask)  # Save mask for testing
    index += 1
    num_pixels = image.shape[0] * image.shape[1]
    #print("Pixelnumber: " + str(num_pixels))

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
    # Rectangle coordinates: (164, 453) to (858, 114)
    #Rectangle coordinates: (861, 442) to (162, 114)
    # Rectangle coordinates: (168, 114) to (860, 447)

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
            print("test2")
            value = point1[0]
            point1 = [point2[0], point1[1]]
            point2 = [value, point2[1]]
            start_point = tuple(point1)
            end_point = tuple(point2)

        # Print the coordinates of the rectangle
        # print(f"Rectangle coordinates: {start_point} to {end_point}")
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

def areaList(imageStack, cutoffB, cutoffG, cutoffR, color_rangelower = 45, color_rangeupper = 250):
    areaList = []
    for i in range(imageStack.shape[0]):
        areaList.append(getArea(imageStack[i], cutoffB, cutoffG, cutoffR, color_rangelower, color_rangeupper))

    return areaList

def output(imageStack, cutoffB = 0, cutoffG = 130, cutoffR = 0, color_rangelower = 45, color_rangeupper = 250):
    xValues = [frametime * i for i in range(imageStack.shape[0])]
    areaValues = areaList(imageStack, cutoffB, cutoffG, cutoffR, color_rangelower, color_rangeupper)
    plt.plot(xValues, areaValues)
    plt.xticks(np.arange(0, len(areaValues)*frametime, 30))

    plt.xlabel('time [s]')
    plt.ylabel('active area [%]')
    plt.show()


def outputWithEchem(imageStack, cutoffB=0, cutoffG=130, cutoffR=0, color_rangelower=45, color_rangeupper=250, echemData=None):
    xValuesImageStack = [frametime * i for i in range(imageStack.shape[0])]
    areaValues = areaList(imageStack, cutoffB, cutoffG, cutoffR, color_rangelower, color_rangeupper)
    label = "test"
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
    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('active area [%]', color=color)
    ax1.plot(xValuesImageStack, areaValues, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.tick_params(axis = 'x', pad = 30)
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel(label, color=color)
    ax2.plot(xdata, ydata, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.show()

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
    areaValues = areaList(imageStack, cutoffB, cutoffG, cutoffR, color_rangelower, color_rangeupper)
    if echemData is not None:
        ydata = []
        xdata = []

        for i in echemData[4][2:]:
            ydata.append(float(i.replace(',', '.')) * 1000000)
        for i in echemData[3][2:]:
            xdata.append(float(i.replace(',', '.')))

    relevantAreaList = areaValues[int(timeDiff/frametime):int(len(ydata)+timeDiff/frametime)]
    currPerArea = [i / j for i, j in zip(ydata, relevantAreaList)]
    plt.plot(currPerArea)
    plt.xticks(np.arange(0, len(ydata)+1, 30))

    plt.xlabel('time [s]')
    plt.ylabel('Current per active area [' + r'$\mu$' + "A/$Area_{\%}$]")
    plt.show()