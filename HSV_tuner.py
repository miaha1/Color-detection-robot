# GUI for tuning HSV values. 
# Run this to adjust the HSV for specific images. 
# press 'q' to quit the window.

import cv2
import numpy as np
import os

# Change this to one of the image number to tune.
IMAGE_PATH = 'data/img23' \
'.jpg' 

def nothing(x):
    pass

# Load the image
image = cv2.imread(IMAGE_PATH)

if image is None:
    print(f"Error: Could not load {IMAGE_PATH}.")
    exit()

# Convert to HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Create a window
cv2.namedWindow('HSV Tuner', cv2.WINDOW_NORMAL)
cv2.resizeWindow('HSV Tuner', 500, 350)

# Create Trackbars
# Hue: Starts at 40 (Lower) and 80 (Upper)
cv2.createTrackbar('L - Hue', 'HSV Tuner', 40, 179, nothing)
cv2.createTrackbar('L - Sat', 'HSV Tuner', 50, 255, nothing)
cv2.createTrackbar('L - Val', 'HSV Tuner', 50, 255, nothing)

cv2.createTrackbar('U - Hue', 'HSV Tuner', 80, 179, nothing)
cv2.createTrackbar('U - Sat', 'HSV Tuner', 255, 255, nothing)
cv2.createTrackbar('U - Val', 'HSV Tuner', 255, 255, nothing)

print("Adjust sliders so the cube is white and background is black.")
print("Press 'q' to quit.")

while True:
    # Get current slider values
    l_h = cv2.getTrackbarPos('L - Hue', 'HSV Tuner')
    l_s = cv2.getTrackbarPos('L - Sat', 'HSV Tuner')
    l_v = cv2.getTrackbarPos('L - Val', 'HSV Tuner')

    u_h = cv2.getTrackbarPos('U - Hue', 'HSV Tuner')
    u_s = cv2.getTrackbarPos('U - Sat', 'HSV Tuner')
    u_v = cv2.getTrackbarPos('U - Val', 'HSV Tuner')

    lower_bound = np.array([l_h, l_s, l_v])
    upper_bound = np.array([u_h, u_s, u_v])

    # Create Mask
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    # Combine the mask with original image to see the color
    result = cv2.bitwise_and(image, image, mask=mask)

    # Show images next to each other for easy comparison
    mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    stacked = np.hstack((image, mask_3ch, result))
    
    scale_percent = 50
    width = int(stacked.shape[1] * scale_percent / 100)
    height = int(stacked.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(stacked, dim, interpolation = cv2.INTER_AREA)

    cv2.imshow('HSV Tuner', resized)

    # 'q' key to exit
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()