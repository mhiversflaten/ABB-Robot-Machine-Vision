import os

from image_tools import Camera
import image_tools.ImageFunctions
from image_tools import ImageFunctions
from RobotWebServices import RWS
import OpenCV_to_RAPID
import random
import threading

robtarget_pucks = []
puck_to_RAPID = 0

#########################################################
#      First, use OpenCV to initialize the camera       #
#         or use the Camera class given if you          #
#              prefer to use uEye API                   #
#########################################################
# ----------------insert code here--------------------- #

#########################################################
#       Second, initialize robot communication,         #
#       start motors and execute RAPID program          #
#########################################################
# ----------------insert code here--------------------- #


"""This will (when completed) calculate the slope which represents how much the lens of the camera is angled.
This should be done by comparing two images taken from different heights.
"""
print("---Running camera_adjustment---")

# Creating a text file for calculations done throughout this program.
# Will be closed and disappear after program is finished
adjustment_file = open('camera_adjustment_XS.txt', 'w')

#########################################################
#       Create a loop where you compare a certain       #
#    amount of images and check if robot is running     #
#########################################################
# ----------------insert code here--------------------- #

i = 0
while robot.is_running() and i < 25:  # Compare images 25 times
    i += 1

    #########################################################
    #      Start the camera adjustment CASE in RAPID        #
    #  remember to wait for RAPID after entering the case   #
    #########################################################
    # ----------------insert code here--------------------- #
    robot.set_rapid_variable("WPW", 5)  # Start camera adjustment procedure in RAPID
    robot.wait_for_rapid()

    #########################################################
    #    Find the puck that will be used for comparison     #
    #      If you find it difficult to detect a puck,       #
    #   try and capture and check for QR-codes in a loop    #
    #                 (overview - 500mm)                    #
    #########################################################
    #           Use OpenCV to capture an image              #
    #         or use your capture image function            #
    #           if you prefer to use uEye API               #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #          Scan the image with your QR_Scanner          #
    #           Place the QR code in a puck list            #
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
    #               puck to the puck_list                   #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #           Create robtargets for the puck              #
    #    (Combine all known offsets to make a robtarget)    #
    #########################################################
    #  Perform transformations to match RAPID coordinates   #
    #########################################################
    # ----------------insert code here--------------------- #

    # Converts puck position from pixels to millimeters
    pixel_to_mm(gripper_height=gripper_height, puck=puck, image=image)

    # Compensate for possibly angled camera
    if not cam_comp:
        camera_compensation(gripper_height=gripper_height, gripper_rot=gripper_rot, puck=puck)

    # Add the offset from camera to gripper
    puck.set_position(position=[puck.position[0] + cam_pos[0], puck.position[1] + cam_pos[1]])

    return puck








    #########################################################
    #           Update robtarget and tell RAPID             #
    #               that image is processed                 #
    #########################################################
    # ----------------insert code here--------------------- #

    robot.set_robtarget_translation("puck_target", robtarget_pucks[0].get_xyz())
    robot.set_rapid_variable("image_processed", "TRUE")

    #########################################################
    #    Do the same steps as above to find a puck once     #
    #    again, the difference being this will be a more    #
    #   accurate representation of the robtarget because    #
    #  of the image being grabbed closer to the puck        #
    #                        tips:                          #
    #    it might be smart to remove the found puck from    #
    #      the list to easily identify the "new" puck       #
    #########################################################
    # ----------------insert code here--------------------- #
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