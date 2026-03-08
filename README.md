
# Cozmo Cube Detection and Tracker

This project enables an Anki Cozmo robot to autonomously search for, track, and drive toward a target object (a cube) using OpenCV and the Cozmo Python SDK. The robot uses a proportional control algorithm to smoothly steer toward the cube and stops automatically when it determines it is close enough.

Designed as a perception module for a **Cozmo robot**, the color thresholds and blob detection parameters were tuned using a dataset of 100 images captured directly from Cozmo's onboard camera. Ultimately, this code enables the robot to perceive and interact with specific colored objects in its environment.

It relies on HSV color segmentation, morphological image processing, and blob detection to accurately identify the target objects.
A HSV Tuner is also developed to help tuning process faster.

## Dataset & Hardware Context

The computer vision pipeline was developed and tested against a custom dataset consisting of 100 images taken from the perspective of a Cozmo robot. Because the images come from a mobile robot's camera, the script is tailored to handle the unique lighting conditions, angles, and camera resolution that Cozmo experiences while navigating. Across this dataset, the detection algorithm achieved a **99% accuracy rate**, correctly identifying the cubes in 99 out of the 100 test images.

!! Note on iOS Compatibility & Grayscale Workaround
During development, a clash between the Cozmo app and iOS resulted in the robot's camera stream outputting exclusively in grayscale, breaking standard color-based object detection.

**The Solution**: Instead of relying on Hue and Saturation for color tracking, the computer vision pipeline was temporarily recalibrated to track the specific grayscale intensity (the 'Value' in the HSV color space) of the target cube.

**Result**: The workaround successfully restores the robot's ability to detect the cube's contrast against the background.

# Project Structure
find_cube.py: Contains the core computer vision logic.

filter_image(): Converts the image to HSV and applies masks/morphological filters.

detect_blob(): Uses cv2.SimpleBlobDetector to find valid targets based on area and inertia.

find_cube(): Main helper function that returns the [x, y, radius] coordinates of the detected cube.

Go_to_cube.py: The main Cozmo execution script. Handles camera initialization, the main event loop, custom viewer annotations (BoxAnnotator), and the motor control logic.

# How to run

Make sure to the robot is in SDK, connect through robot's wifi.
```bash
python Go_to_cube.py
