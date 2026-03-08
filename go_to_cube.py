#!/usr/bin/env python3
#!c:/Python35/python3.exe -u
import sys
import cv2
import numpy as np
import cozmo
import time
import os
from glob import glob
import asyncio
from find_cube import *

try:
    from PIL import ImageDraw, ImageFont
except ImportError:
    sys.exit('run `pip3 install --user Pillow numpy` to run this example')
def nothing(x):
    pass

YELLOW_LOWER = np.array([9, 115, 151])
YELLOW_UPPER = np.array([179, 215, 255])

# values for green cube but in gray scale
# GREEN_LOWER = np.array([0,0,0])
# GREEN_UPPER = np.array([179, 255, 60])

# values for green cube but in gray scale
GGL_H,GGL_S,GGL_V = 0,0,6
GREEN_LOWER = np.array([GGL_H/2, GGL_S*255//100, GGL_V*255//100])
GGU_H,GGU_S,GGU_V = 0,0,25
GREEN_UPPER = np.array([GGU_H/2, GGU_S*255//100, GGU_V*255//100])

# Define a decorator as a subclass of Annotator; displays the keypoint
class BoxAnnotator(cozmo.annotate.Annotator):

    cube = None

    def apply(self, image, scale):
        d = ImageDraw.Draw(image)
        bounds = (0, 0, image.width, image.height)

        if BoxAnnotator.cube is not None:

            #double size of bounding box to match size of rendered image
            BoxAnnotator.cube = np.multiply(BoxAnnotator.cube,2)

            #define and display bounding box with params:
            box = cozmo.util.ImageBox(BoxAnnotator.cube[0]-BoxAnnotator.cube[2]/2,
                                      BoxAnnotator.cube[1]-BoxAnnotator.cube[2]/2,
                                      BoxAnnotator.cube[2], BoxAnnotator.cube[2])
            cozmo.annotate.add_img_box_to_image(image, box, "green", text=None)

            BoxAnnotator.cube = None



async def run(robot: cozmo.robot.Robot):

    robot.world.image_annotator.annotation_enabled = False
    robot.world.image_annotator.add_annotator('box', BoxAnnotator)

    robot.camera.color_image_enabled = True
    robot.camera.image_stream_enabled = True
    robot.camera.enable_auto_exposure = True

    fixed_gain, exposure, mode = 390,3,1

    try:

        while True:

            #get camera image
            event = await robot.world.wait_for(cozmo.world.EvtNewCameraImage, timeout=30)

            if event.image is not None:

                img = np.asarray(event.image.raw_image)
                image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                if mode == 1:
                    robot.camera.enable_auto_exposure = True
                else:
                    robot.camera.set_manual_exposure(exposure,fixed_gain)

                #find the cube
                cube = find_cube(image, GREEN_LOWER, GREEN_UPPER)
                print(cube)
                BoxAnnotator.cube = cube

                ################################################################
                # Motion Control Logic:
                ################################################################
                # Check if a cube was detected
                if cube is not None and len(cube) >= 3:
                    # Extract the cube's center X and its size from find_cube output
                    # cube format is [center_x, center_y, size]
                    cube_x = cube[0] 
                    cube_size = cube[2]
                    
                    # Get the center of the camera image
                    image_center_x = image.shape[1] / 2
                    
                    # Calculate how far off-center the cube is
                    error_x = cube_x - image_center_x
                    
                    # --- Control Parameters ---
                    k_p = 0.3          # Proportional gain for turning
                    base_speed = 35    # Forward speed in mm/s
                    target_size = 60  # Bounding box size that means "close enough"
                    
                    if cube_size > target_size:
                        # Stop moving if the cube is close enough. 
                        await robot.drive_wheels(0, 0)
                    else:
                        # Steer towards the cube while driving forward
                        # If error_x is positive (cube is to the right), left wheel speeds up, right slows down
                        l_wheel_speed = base_speed + (error_x * k_p)
                        r_wheel_speed = base_speed - (error_x * k_p)
                        
                        await robot.drive_wheels(l_wheel_speed, r_wheel_speed)
                else:
                    # No cube found in the current frame. Spin in place to search.
                    await robot.drive_wheels(20, -20)


    except KeyboardInterrupt:
        print("")
        print("Exit requested by user")
    except cozmo.RobotBusy as e:
        print(e)

if __name__ == '__main__':
    cozmo.run_program(run, use_viewer = True, force_viewer_on_top = True)
