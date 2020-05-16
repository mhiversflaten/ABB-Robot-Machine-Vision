import numpy as np
import configparser
from image_tools import ImageFunctions
import os
import math
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pyzbar.wrapper import ZBarSymbol
import Puck
from image_tools import Camera
from pyueye import ueye
import time
import OpenCV_to_RAPID


def quaternion_to_radians(quaternion):
    """Complete function to convert a Quaternion to a rotation about the z-axis in degrees.
    """
    w, x, y, z = quaternion
    t1 = +2.0 * (w * z + x * y)
    t2 = +1.0 - 2.0 * (y * y + z * z)
    rotation_z = math.atan2(t1, t2)

    return rotation_z

def camera_adjustment(cam, robot):
    """Calculates the slope which represents how much the lens of the camera is angled.
    This is done by comparing two images taken from different heights.
    """
    print("---Running camera_adjustment---")

    abspath = os.path.abspath("image_tools/cam_adjustments.ini")

    adjustment_file = open('camera_adjustment_XS.txt', 'w')

    i = 0
    while robot.is_running() and i < 25:  # Compare images 25 times
        i += 1
        robot.set_rapid_variable("WPW", 5)  # Start camera adjustment procedure in RAPID

        robot.wait_for_rapid()

        # List with robtarget for the found puck
        robtarget_pucks = []

        #########################################################
        # First, find the puck that will be used for comparison #
        #########################################################
        # ----------------insert code here--------------------- #

        while not robtarget_pucks:
            ImageFunctions.findPucks(cam, robot, robtarget_pucks, cam_comp=True)
        print("xyz:", robtarget_pucks[0].get_xyz())

        robot.set_robtarget_translation("puck_target", robtarget_pucks[0].get_xyz())
        robot.set_rapid_variable("image_processed", "TRUE")

        robtarget_pucks.clear()

        robot.wait_for_rapid()

        # Close-up image of puck (working distance = 100mm)
        while not robtarget_pucks:
            ImageFunctions.findPucks(cam, robot, robtarget_pucks, cam_comp=True)

        robot.set_rapid_variable("image_processed", "TRUE")

        pos_low = robtarget_pucks[0].get_xyz()
        print(f'Low robtarget: ({pos_low[0]:.1f},{pos_low[1]:.1f})')

        robot.wait_for_rapid()

        robtarget_pucks.clear()

        # Image of puck from a higher position (working distance = 540)
        while not robtarget_pucks:
            ImageFunctions.findPucks(cam, robot, robtarget_pucks, cam_comp=True)

        pos_high = robtarget_pucks[0].get_xyz()
        print(f'High robtarget: ({pos_high[0]:5.1f},{pos_high[1]:5.1f})')

        delta_h = 540 - 100  # Heights are set in RAPID script
        delta_x = pos_high[0] - pos_low[0]
        delta_y = pos_high[1] - pos_low[1]
        print(f'Delta: ({delta_x:5.1f}, {delta_y:5.1f})')

        slope_x = delta_x / delta_h
        slope_y = delta_y / delta_h

        # Write all slope values to .txt-file
        if robot.is_running():
            adjustment_file.write(f'{slope_x:.4f},{slope_y:.4f}\n')

    adjustment_file.close()

    # Get all slope values and find the average
    contents = np.genfromtxt(r'camera_adjustment_XS.txt', delimiter=',')
    os.remove('camera_adjustment_XS.txt')

    sum_slope_x = 0
    sum_slope_y = 0
    for content in contents:
        sum_slope_x += content[0]
        sum_slope_y += content[1]

        # TODO: Find out why absolute value was used previously:
        """
        sum_slope_x += abs(content[0])
        sum_slope_y += abs(content[1])"""

    average_slope_x = sum_slope_x / len(contents)
    average_slope_y = sum_slope_y / len(contents)

    configfile_name = abspath

    Config = configparser.ConfigParser()
    Config.read(configfile_name)

    cfgfile = open(configfile_name, 'w')

    # Add content to the file
    Config.set('SLOPE', 'slopex', f'{average_slope_x:.4f}')
    Config.set('SLOPE', 'slopey', f'{average_slope_y:.4f}')
    Config.write(cfgfile)

    cfgfile.close()


def findPucks(cam, robot, robtarget_pucks, cam_comp=False, number_of_images=1, pucks_in_height=False):
    """Finds all pucks in the frame of the camera by capturing an image and scanning the image for QR codes.
    After the codes have been pinpointed, a series of transformations happen to finally create robtargets
    which can be sent to RobotWare.
    """

    trans, gripper_rot = robot.get_gripper_position()
    gripper_height = robot.get_gripper_height()

    cam_pos = OpenCV_to_RAPID.get_camera_position(trans=trans, rot=gripper_rot)

    for _ in range(number_of_images):

        #########################################################
        #        First, use OpenCV to capture an image          #
        #         or use your capture image function            #
        #           if you prefer to use uEye API               #
        #########################################################
        # ----------------insert code here--------------------- #
        # TODO: De skal bruke OpenCV
        image = capture_image(cam=cam, gripper_height=gripper_height)

        #########################################################
        #          Scan the image with your QR_Scanner          #
        #      Place the QR codes in a temporary puck list      #
        #########################################################
        # ----------------insert code here--------------------- #
        temp_puck_list = QR_Scanner(image)

        # Check if the QR codes that were found have already been located previously.
        # If so, remove them from the temporary list.
        for puck in robtarget_pucks:
            if any(puck == x for x in temp_puck_list):
                temp_puck_list.remove(puck)

        #########################################################
        #         Create robtargets for every new puck          #
        #########################################################
        # ----------------insert code here--------------------- #
        for puck in temp_puck_list:
            puck = OpenCV_to_RAPID.create_robtarget(gripper_height=gripper_height, gripper_rot=gripper_rot,
                                                    cam_pos=cam_pos, image=image, puck=puck, cam_comp=cam_comp,
                                                    pucks_in_height=pucks_in_height)
            robtarget_pucks.append(puck)

    return robtarget_pucks


def capture_image(cam, gripper_height):
    """Captures a single image through PyuEye functions.
    Focus is manually adjusted depending on the working distance.
    """
    #########################################################
    #        Calculate the working distance to pass         #
    #           into the calculate_focus function           #
    #             and finally capture an image              #
    #                 (if using uEye API)                   #
    #########################################################
    # ----------------insert code here--------------------- #

    return img


def QR_Scanner(img):
    """Scan QR codes from image. Returns position, orientation and image with marked QR codes"""

    puck_list = []

    #########################################################
    #  Reduce noise and increase the contrast in the image  #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #              Decode the processed image               #
    #  You can also sort them in ascending order if wanted  #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #  Make a loop to go through all QR codes, and extract  #
    #   two corner points to be able to find the center.    #
    #   Remember to update the Puck object and append the   #
    #        puck to the puck_list you are returning        #
    #########################################################
    # ----------------insert code here--------------------- #

    return puck_list


def create_robtarget(gripper_height, gripper_rot, cam_pos, image, puck, cam_comp=False):
    """Combine all known offsets to make a robtarget on the work object.
    """

    #########################################################
    #  Transform position depending on rotation of gripper  #
    #########################################################
    # ----------------insert code here--------------------- #
    transform_position(gripper_rot=gripper_rot, puck=puck)

    # Converts puck position from pixels to millimeters
    pixel_to_mm(gripper_height=gripper_height, puck=puck, image=image)

    # TODO: De trenger ikke overshoot_comp
    # Compensate for overshoot in 2D image
    overshoot_comp(gripper_height=gripper_height, puck=puck)

    # Compensate for possibly angled camera
    if not cam_comp:
        camera_compensation(gripper_height=gripper_height, gripper_rot=gripper_rot, puck=puck)

    # Add the offset from camera to gripper
    puck.set_position(position=[puck.position[0] + cam_pos[0], puck.position[1] + cam_pos[1]])

    return puck


def transform_position(puck):
    """Transform coordinate system given by image in OpenCV to coordinate system of work object in RAPID by
    swapping x & y coordinates and rotate by the same amount that the camera has been rotated.
    """

    #########################################################
    #  Perform transformations to match RAPID coordinates   #
    #########################################################
    # ----------------insert code here--------------------- #
    puck.set_position(position=[-puck.position[1], -puck.position[0]])


def pixel_to_mm(gripper_height, puck, image):
    """Converts coordinates in image from pixels to millimeters.
    This depends on the camera's working distance.
    """

    # As a good approximation we can say that: sensor width / FOV width = focal length / working distance
    # parameters from the XS camera
    focal_length = 3.7  # mm (+/- 5 percent)
    sensor_width = 3.6288
    resolution_width = image.shape[1]

    working_distance = gripper_height + 70

    fov_width = (working_distance / focal_length) * sensor_width

    pixel_to_mm = fov_width / resolution_width  # mm_width / px_width

    # Convert all positions from pixels to millimeters:
    puck.set_position(position=[x * pixel_to_mm for x in puck.position])