import os
import numpy as np

robtarget_pucks = []

#########################################################
#      First, use OpenCV to initialize the camera       #
#         or use the Camera class given if you          #
#              prefer to use uEye API                   #
#########################################################
# ----------------insert code here--------------------- #

#########################################################
#       Second, initialize robot communication,         #
#              and execute RAPID program                #
#                 (Create RWS object)                   #
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
while i < 5:  # Compare images 5 times
    i += 1

    #########################################################
    #      Start the camera adjustment CASE in RAPID        #
    #  remember to wait for RAPID after entering the case   #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #  Capture image, process it and scan it for QR codes   #
    #     Do this several times if no QR code is found      #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #    Create a robtarget from the QR codes' position     #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #               Send the robtarget to RAPID             #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #    Tell RAPID to move to a close-up image position    #
    #               (Update flag variable)                  #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #       Wait for robot to reach close-up position       #
    #  Capture image, process it and scan it for QR codes   #
    #     Do this several times if no QR code is found      #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #                Create a robtarget                     #
    #            from the QR codes' position                #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #      Save the translation of the "low" robtarget      #
    #        (will be used later to calculate slope)        #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #     Tell RAPID to go straight up to new height        #
    #               (Update flag variable)                  #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #  Again, capture an image and calculate the robtarget  #
    #             (as done in previous steps)               #
    #########################################################
    # ----------------insert code here--------------------- #

    #########################################################
    #   Save the translation of the "high" robtarget puck   #
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
    slope_x = None
    slope_y = None

    # Write all slope values to .txt-file
    adjustment_file.write(f'{slope_x:.4f},{slope_y:.4f}\n')

adjustment_file.close()

contents = np.genfromtxt(r'camera_adjustment_XS.txt', delimiter=',')
os.remove('camera_adjustment_XS.txt')

sum_slope_x = 0
sum_slope_y = 0
for content in contents:
    sum_slope_x += content[0]
    sum_slope_y += content[1]

average_slope_x = sum_slope_x / len(contents)
average_slope_y = sum_slope_y / len(contents)
"""These slopes is what you will need to compensate for 
the camera position error for more accurate picking."""
