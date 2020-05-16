import os

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
    #                 (overview position)                   #
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

    ################################################################
    #               Create robtargets for the puck                 #
    #        (Combine all known offsets to make a robtarget)       #
    ################################################################
    #      Perform transformations to match RAPID coordinates      #
    ################################################################
    #          As a good approximation we can say that:            #
    #  sensor width / FOV width = focal length / working distance  #
    ################################################################
    #        Here are some parameters from the XS camera:          #
    ################################################################
    focal_length = 3.7  # mm (+/- 5 percent)
    sensor_width = 3.6288
    resolution_width = image.shape[1]

    #########################################################
    #      With the help of the values above, and the       #
    #   explanation in the assignment, convert the pixel    #
    #     values to mm to be used in making a robtarget     #
    #########################################################
    #   Remember: Update the positions by multiplying the   #
    #    found conversion with the found pixel position     #
    #########################################################
    # ----------------insert code here--------------------- #

    # TODO: How is this done for them (if not using Puck class)? Is this explained in LAB Assignment?
    # Add the offset from camera to gripper
    puck.set_position(position=[puck.position[0] + cam_pos[0], puck.position[1] + cam_pos[1]])

    #########################################################
    #           Update robtarget and tell RAPID             #
    #               that image is processed                 #
    #########################################################
    # ----------------insert code here--------------------- #

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

    #########################################################
    #  Retrieve the translation of the "low" robtarget puck #
    #        (will be used later to calculate slope)        #
    #########################################################
    # ----------------insert code here--------------------- #
    pos_low = robtarget_pucks[0].get_xyz()
    print(f'Low robtarget: ({pos_low[0]:.1f},{pos_low[1]:.1f})')
    robot.wait_for_rapid()
    robtarget_pucks.clear()

    #########################################################
    #    Find puck (grab image) from a higher position      #
    #       above the puck and convert to robtarget         #
    #             (as done in previous steps)               #
    #                        tips:                          #
    #    it might be smart to remove the found puck from    #
    #      the list to easily identify the "new" puck       #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    # Retrieve the translation of the "high" robtarget puck #
    #        (will be used later to calculate slope)        #
    #########################################################
    # ----------------insert code here--------------------- #

    ###########################################################
    #       Calculate the delta height, as well as the        #
    #             delta in both x and y position              #
    # (Compare the "high" robtarget with the "low" robtarget) #
    ###########################################################
    # -----------------insert code here---------------------- #

    #########################################################
    #       Find the slope in both x and y direction        #
    #########################################################
    # ----------------insert code here--------------------- #

    # Write all slope values to .txt-file
    if robot.is_running():
        adjustment_file.write(f'{slope_x:.4f},{slope_y:.4f}\n')

adjustment_file.close()

#########################################################
#    Use the slope values in the adjustment.txt file    #
#      and calculate the average slope in x and y       #
#########################################################
#        These slopes is what you will need to          #
#   "calibrate" the camera for more accurate picking    #
#########################################################
# ----------------insert code here--------------------- #
contents = np.genfromtxt(r'camera_adjustment_XS.txt', delimiter=',')
os.remove('camera_adjustment_XS.txt')

sum_slope_x = 0
sum_slope_y = 0
for content in contents:
    sum_slope_x += content[0]
    sum_slope_y += content[1]

average_slope_x = sum_slope_x / len(contents)
average_slope_y = sum_slope_y / len(contents)