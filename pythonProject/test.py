import cv2

# Global variables to store the coordinates
start_point = None
end_point = None
drawing = False
image = None

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
        cv2.rectangle(image, start_point, end_point, (0, 255, 0), 2)
        cv2.imshow("Image", image)

        # Print the coordinates of the rectangle
        print(f"Rectangle coordinates: {start_point} to {end_point}")

# # Load an image
# image = cv2.imread('testimg.tif')
# if image is None:
#     print("Could not read the image.")
#     exit()
#
# # Create a window and set the mouse callback
# cv2.namedWindow("Image")
# cv2.setMouseCallback("Image", draw_rectangle)
#
# while True:
#     cv2.imshow("Image", image)
#     key = cv2.waitKey(1)
#
#     # Break the loop when 'q' is pressed
#     if key == ord('q'):
#         break
#
# # Cleanup
# cv2.destroyAllWindows()
