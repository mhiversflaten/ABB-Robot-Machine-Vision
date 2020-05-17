# place needed imports

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

while robot.is_running():  # Run script while RAPID execution is running
    print("""
        Choose what to do:
        1: Pick and place a single puck
        0: Exit
        """)

    userinput = int(input('\nWhat should RAPID do?: '))

    if userinput == 1:
        """
        Pick up and place a chosen puck to a chosen location. 
        Captures an image and finds all pucks in the work area.
        The user is prompted to select puck and location.
        Uses collision avoidance when picking up puck.
        """

        print("Pick and place a single puck")

        #########################################################
        #     Start wanted case in RAPID and wait for RAPID     #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #         Use or create a findPucks function to         #
        #              find and create robtargets               #
        #   If several pucks are to be found, try and capture   #
        #  X amount of images to ensure all pucks are detected  #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #               Figure out how to choose a              #
        #              specified puck by user input             #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #       Extract the selected puck from the puck         #
        #      list you created and retrieve its coordinates    #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #      Use the coordinates grabbed and transfer to      #
        #      RAPID to be able to move closer to the puck      #
        #                        tips:                          #
        #    it might be smart to remove the found puck from    #
        #      the list to easily identify the "new" puck       #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #       Choose where the puck should be moved to        #
        # It can be a predefined position, or a user input one  #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #     Capture images until the puck is found again      #
        #  this time with a close-up image for better accuracy  #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #    Extract the  coordinates again, and transfer to    #
        #         RAPID to be able to pick up the puck          #
        #                       tips:                           #
        #    it might be smart to remove the found puck from    #
        #      the list to easily identify the "new" puck       #
        #########################################################
        # ----------------insert code here--------------------- #

    elif userinput == 0:
        print("Exiting Python program and turning off robot motors")
        robot.stop_RAPID()
        robot.motors_off()