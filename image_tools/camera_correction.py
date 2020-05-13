import numpy as np
import configparser
from image_tools.QR_Reader import QR_Scanner
from pyueye import ueye
from numpy import median
from image_tools import ImageFunctions
import os
import sys


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

        robtarget_pucks = []

        # First, find the puck that will be used for comparison
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


def find_correct_exposure(cam, robot):
    """Auto exposure is not used, as it may fail to identify what the subject is.
    Instead, a manual exposure value is calculated by capturing images with all possible
    exposure values and selecting the value that identifies QR codes with most success.
    """

    # If the repeatability test fails, this will exit the program
    if not robot.is_running():
        sys.exit(0)

    print("---Running find_correct_exposure---")

    # TODO: Use several pucks to determine the best exposure times.
    #  Input amount of pucks and grade exposure values based on how many of the pucks are found each time

    robot.set_rapid_variable("WPW", 10)

    abspath = os.path.abspath("image_tools/cam_adjustments.ini")

    exposure_values = []
    puck_list = []
    # Exposure range (in ms)
    exposure_low = 1
    exposure_high = 66

    increment = 2
    # Loop from lowest possible exposure to highest possible exposure, incremented by 2 (ms)
    for exposure in range(exposure_low, exposure_high, increment):
        # Set new exposure
        newExposure = ueye.DOUBLE(exposure)
        ret = ueye.is_Exposure(cam.hCam, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, newExposure, ueye.sizeof(newExposure))

        img = ImageFunctions.capture_image(cam=cam, gripper_height=500)
        puck_list = QR_Scanner(img)
        print("Found puck:", puck_list)

        # Checking exposure
        d = ueye.DOUBLE()
        retVal = ueye.is_Exposure(cam.hCam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, d, 8)
        if retVal == ueye.IS_SUCCESS:
            print('Currently set exposure time %8.3f ms' % d)

        # Position returns as None if no QR-code is found
        if puck_list:
            exposure_values.append((exposure, len(puck_list)))

    weighted_sum = 0
    pucks_found = 0
    for value_pair in exposure_values:
        pucks_found += value_pair[1]
        weighted_sum += value_pair[0] * value_pair[1]

    exposure = str(int(weighted_sum / pucks_found))

    #exposure = str(median(exposure_values[0]))
    print(exposure_values[0])

    configfile_name = abspath

    config = configparser.ConfigParser()
    config.read(configfile_name)
    cfgfile = open(configfile_name, 'w')

    # Add content to the file
    config.set('EXPOSURE', 'exposure', exposure)
    config.write(cfgfile)

    cfgfile.close()

    # Set the correct exposure time
    cam.set_parameters()
