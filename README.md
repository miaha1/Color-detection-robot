# Color-detection-robot
# Cozmo Cube Detection and Counting 

This project provides a Python script (`count_cubes.py`) that utilizes OpenCV and NumPy to automatically detect and count colored cubes. Designed as a perception module for a **Cozmo robot**, the color thresholds and blob detection parameters were tuned using a dataset of 100 images captured directly from Cozmo's onboard camera. Ultimately, this code enables the robot to perceive and interact with specific colored objects in its environment.

It relies on HSV color segmentation, morphological image processing, and blob detection to accurately identify the target objects.
A HSV Tuner is also developed to help tuning process faster.

## Dataset & Hardware Context

The computer vision pipeline was developed and tested against a custom dataset consisting of 100 images taken from the perspective of a Cozmo robot. Because the images come from a mobile robot's camera, the script is tailored to handle the unique lighting conditions, angles, and camera resolution that Cozmo experiences while navigating. Across this dataset, the detection algorithm achieved a **99% accuracy rate**, correctly identifying the cubes in 99 out of the 100 test images.

## Current Capabilities & Future Work

Currently, the script is configured with specific HSV thresholds to detect **yellow** (including standard and washed-out variants) and **green** cubes. 

**Planned Enhancements:**
* **Expanded Color Palette:** Add HSV bounding arrays and filtering logic to detect and count additional colors (e.g., red, blue, orange).
* **Code Refactoring:** Transition from hardcoded color bounds to a configuration dictionary, allowing new colors to be added simply by defining their name and HSV range.
