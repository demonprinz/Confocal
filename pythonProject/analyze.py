# Version 1.0
# author: Patrick Scholz Contact: patrick.alexander.scholz@rwth-aachen.de
# currently intended to work for up to 99 simultaneously measured channels, files must be in *.tif format
# Image file name format: SeriesXXX_tYYY_z0_chZZ with XXX as increment of the run per day, YYY as timeframe and ZZ as Channel number
# for now the only hard requirement for the name format is the name ends with chZZ.tif

#import modules
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Global variables to store the coordinates
start_point = None
end_point = None
drawing = False
image = None


def getArea(image, cutoffB, cutoffG, cutoffR, color_rangelower = 45, color_rangeupper = 250):
    #image = cv2.imread("test.png")
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


def crop(image, x, x1, y, y1):
    croped_image = image[y:y1, x:x1]
    cv2.imshow("Test", croped_image)


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
        cv2.rectangle(image, start_point, end_point, (200, 0, 0), 2)
        cv2.imshow("Image Cropper", image)

        # Print the coordinates of the rectangle
        print(f"Rectangle coordinates: {start_point} to {end_point}")
        print(start_point[0], end_point[1])
        crop(image, start_point[0], end_point[0], start_point[1], end_point[1])

def cropper(img):
    # Create a window and set the mouse callback
    global image
    cv2.namedWindow("Image Cropper")
    image = img
    cv2.setMouseCallback("Image Cropper", draw_rectangle)

    while True:
        cv2.imshow("Image Cropper", image)
        key = cv2.waitKey(1)

        # Break the loop when 'q' is pressed
        if key == ord('q'):
            break

    # Cleanup
    cv2.destroyAllWindows()