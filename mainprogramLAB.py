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
        #      if you want to be able to pick it up again       #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #       Choose where the puck should be moved to        #
        # It can be a predefined position, or a user input one  #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #      Use the coordinated grabbed and transfer to      #
        #      RAPID to be able to move closer to the puck      #
        #                        tips:                          #
        #    it might be smart to remove the found puck from    #
        #      the list to easily identify the "new" puck       #
        #      if you want to be able to pick it up again       #
        #########################################################
        # ----------------insert code here--------------------- #

        # Capture images until the puck is found again in the close-up image
        while not any(pucknr == x.number for x in robtarget_pucks):
            ImageFunctions.findPucks(cam, norbert, robtarget_pucks)

        # Extract the selected puck from the puck list -> puck_to_RAPID
        for puck in robtarget_pucks:
            if puck.number == pucknr:
                puck_to_RAPID = puck
                break

        norbert.set_rapid_variable("gripper_angle", rotation)
        offset_x, offset_y = OpenCV_to_RAPID.gripper_camera_offset(rot)
        if forward_grip:
            norbert.set_rapid_array("gripper_camera_offset", (offset_x, offset_y))
        else:
            norbert.set_rapid_array("gripper_camera_offset", (-offset_x, -offset_y))
        norbert.set_robtarget_translation("puck_target", puck_to_RAPID.get_xyz())
        norbert.set_rapid_variable("image_processed", "TRUE")  # Robot may pick and place selected puck

        robtarget_pucks.remove(puck_to_RAPID)  # Remove puck so that it may be added to the list again later
    elif userinput == 0:
        print("Exiting Python program and turning off robot motors")
        robot.stop_RAPID()
        robot.motors_off()