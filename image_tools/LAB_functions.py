import os
import numpy as np

def camera_adjustment(cam, robot):
    """Calculates the slope which represents how much the lens of the camera is angled.
    This is done by comparing two images taken from different heights.
    """
    print("---Running camera_adjustment---")

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
        #                 (create a function)                   #
        #       make sure to tell RAPID that the image is       #
        # processed after you have found and created robtargets #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #  Second, find the puck once again while closer to it  #
        #           (use the created function again)            #
        #########################################################
        #  Retrieve the translation of the "low" robtarget puck #
        #        (will be used later to calculate slope)        #
        #########################################################
        #       make sure to tell RAPID that the image is       #
        # processed after you have found and created robtargets #
        #                        tips:                          #
        #    it might be smart to remove the found puck from    #
        #      the list to easily identify the "new" puck       #
        #########################################################
        # ----------------insert code here--------------------- #

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

    # This gathers the content from the txt file, and removes the file after
    # If you do not want it removed, simply comment out the os.remove line
    contents = np.genfromtxt(r'camera_adjustment_XS.txt', delimiter=',')
    os.remove('camera_adjustment_XS.txt')

    #########################################################
    #       Print or return the found average slopes        #
    # these will be used to correct the camera for any tilt #
    #########################################################

def findPucks(cam, robot, robtarget_pucks, cam_comp=False, number_of_images=1, pucks_in_height=False):
    """Finds all pucks in the frame of the camera by capturing an image and scanning the image for QR codes.
    After the codes have been pinpointed, a series of transformations happen to finally create robtargets
    which can be sent to RobotWare.
    """

    for _ in range(number_of_images):

        #########################################################
        #        First, use OpenCV to capture an image          #
        #         or use your capture image function            #
        #           if you prefer to use uEye API               #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #          Scan the image with your QR_Scanner          #
        #           Place the QR codes in a puck list           #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #    Create robtargets for the new puck (or several)    #
        #########################################################
        # ----------------insert code here--------------------- #

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
    #       Transform positions (create a function)         #
    #########################################################
    # ----------------insert code here--------------------- #
    transform_position(gripper_rot=gripper_rot, puck=puck)

    #########################################################
    #      Convert from pixel to mm (create a function)     #
    #########################################################
    # ----------------insert code here--------------------- #

    # TODO: How is this done for them (if not using Puck class)? Is this explained in LAB Assignment?
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
    ################################################################
    #          As a good approximation we can say that:            #
    #  sensor width / FOV width = focal length / working distance  #
    ################################################################
    #        Here are some parameters from the XS camera           #
    ################################################################
    focal_length = 3.7  # mm (+/- 5 percent)
    sensor_width = 3.6288
    resolution_width = image.shape[1]

    #########################################################
    #      With the help of the values above, and the       #
    #   explanation in the task, convert the pixel values   #
    #        to mm to be used in making a robtarget         #
    #########################################################
    #   Remember: Update the positions by multiplying the   #
    #    found conversion with the found pixel position     #
    #########################################################
    # ----------------insert code here--------------------- #

    working_distance = gripper_height + 70

    fov_width = (working_distance / focal_length) * sensor_width

    pixel_to_mm = fov_width / resolution_width  # mm_width / px_width

    # Convert all positions from pixels to millimeters:
    puck.set_position(position=[x * pixel_to_mm for x in puck.position])