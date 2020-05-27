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
#                 (Create RWS object)                   #
#########################################################
# ----------------insert code here--------------------- #

while True:  # Run script indefinitely
    print("""
        Choose what to do:
        1: Pick and place a single puck
        0: Exit
        """)
    # Program may be extended

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
        #         Create a (more accurate) robtarget            #
        #            from the QR codes' position                #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #               Send the robtarget to RAPID             #
        #########################################################
        # ----------------insert code here--------------------- #

        #########################################################
        #           Tell RAPID to pick up and place puck        #
        #               (Update flag variable)                  #
        #########################################################
        # ----------------insert code here--------------------- #

    elif userinput == 0:
        print("Exiting Python program and turning off robot motors")
        #########################################################
        #   Start RAPID execution and switch off robot motors   #
        #                (Use RWS functions)                    #
        #########################################################
        # ----------------insert code here--------------------- #
        break