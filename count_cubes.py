import cv2
import numpy as np

# Modify these values for yellow color range. Add thresholds for detecting green also.

# standard yellow
yellow_lower_1 = np.array([6, 177, 130])
yellow_upper_1 = np.array([18, 255, 255])

# bright/washed-out yellow 
yellow_lower_2 = np.array([13, 115, 190])
yellow_upper_2 = np.array([23, 255, 255])

# green
green_lower = np.array([17, 2, 10])
green_upper = np.array([109, 255, 255])

# Change this function so that it filters the image based on color using the hsv range for each color.
def filter_image(img, hsv_lower, hsv_upper):
    # convert BRG image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Modify mask

    mask = cv2.inRange(hsv,hsv_lower, hsv_upper) 

    # This kernel will merge pieces that are close together
    kernel = np.ones((5,5), np.uint8)

    # MORPH_CLOSE closes gaps inside the object
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # MORPH_OPEN removes noise from the background
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    return mask
    
# Change the parameters to make blob detection more accurate.
def detect_blob(mask):

# smooth the image to reduce noise and improve blob detection
    img = cv2.medianBlur(mask, 5)

    # Set up the SimpleBlobdetector with default parameters.
    params = cv2.SimpleBlobDetector_Params()

    # The mask has white blobs (255) on black background (0).
    params.filterByColor = True
    params.blobColor = 255

    # filter by area
    params.filterByArea = True
    params.minArea = 153   
    params.maxArea = 100000

    # Filter by shape (Noise Removal)
    
    params.filterByCircularity = False

    params.filterByConvexity = False

    params.filterByInertia = True
    params.minInertiaRatio = 0.1

    # builds a blob detector with the given parameters 
    detector = cv2.SimpleBlobDetector_create(params)

    # use the detector to detect blobs.
    keypoints = detector.detect(img)

    return len(keypoints)
    
def count_cubes(img):

    # Mask 1: Standard Yellow
    mask_yellow_1 = filter_image(img, yellow_lower_1, yellow_upper_1)
    
    # Mask 2: Bright/Washed-out Yellow
    mask_yellow_2 = filter_image(img, yellow_lower_2, yellow_upper_2)
    
    # Combine: If a pixel is in Mask 1 OR Mask 2, it counts as yellow.
    mask_yellow_final = cv2.bitwise_or(mask_yellow_1, mask_yellow_2)
    
    num_yellow = detect_blob(mask_yellow_final)

    # green mask
    mask_green = filter_image(img, green_lower, green_upper)
    num_green = detect_blob(mask_green)

    return num_yellow, num_green
