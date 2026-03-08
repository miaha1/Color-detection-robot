import cv2
import numpy as np
import time

def filter_image(img, hsv_lower, hsv_upper):

    # convert BRG image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

    # This kernel will merge pieces that are close together
    kernel = np.ones((5,5), np.uint8)

    # MORPH_CLOSE closes gaps inside the object
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # MORPH_OPEN removes noise from the background
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    return mask
    
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
    # params.minArea = 153   
    params.minArea = 400    
    params.maxArea = 20000

    # Filter by shape (Noise Removal)
    
    params.filterByCircularity = False

    params.filterByConvexity = False

    params.filterByInertia = True
    params.minInertiaRatio = 0.1

    # builds a blob detector with the given parameters 
    detector = cv2.SimpleBlobDetector_create(params)
    # use the detector to detect blobs.
    keypoints = detector.detect(img)

    return keypoints

def find_cube(img, hsv_lower, hsv_upper):
    """Find the cube in an image.
        Arguments:
        img -- the image
        hsv_lower -- the h, s, and v lower bounds
        hsv_upper -- the h, s, and v upper bounds
        Returns [x, y, radius] of the target blob, and [0,0,0] or None if no blob is found.
    """
    mask = filter_image(img, hsv_lower, hsv_upper)
    keypoints = detect_blob(mask)

    if len(keypoints) == 0:
        return None
    
    sorted_keypoints = sorted(keypoints, key=lambda kp: kp.size, reverse=True)
    blob = sorted_keypoints[0]

    x, y = blob.pt
    size = blob.size/2

    output = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255),
                           cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    
    # output the detected blob
    cv2.imwrite("output.jpg", output)

    return [x, y, size]
