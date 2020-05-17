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
        1: *for you to choose*
        2: *for you to choose*
        3: *for you to choose*
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

        norbert.set_rapid_variable("WPW", 1)  # Start same CASE in RAPID
        norbert.wait_for_rapid()  # Robot goes to overview position

        # Capture X amount of images to ensure that all pucks are found
        robtarget_pucks = ImageFunctions.findPucks(cam, norbert, robtarget_pucks, number_of_images=5)

        if not robtarget_pucks:
            print('Could not find any pucks! Check exposure and focus values before trying again.')
            continue

        # Sort pucks in ascending order
        robtarget_pucks.sort(key=lambda x: x.number)

        print("Found pucks: ", end='')
        print(*robtarget_pucks, sep=', ')

        puck_numbers = []
        for puck in robtarget_pucks:
            puck_numbers.append(puck.number)

        # Select puck that should be moved
        while True:
            print('Which puck should be moved? Options: "', end='')
            print(*puck_numbers, sep='", "', end='"')
            try:
                pucknr = int(input(': '))
            except ValueError:
                print('Input must be an integer. Try again.')
                continue
            if pucknr in puck_numbers:  # Success
                break
            else:
                print('Wrong input, please try again.')
                continue

        # Extract the selected puck from the puck list -> puck_to_RAPID
        for puck in robtarget_pucks:
            if puck.number == pucknr:
                puck_to_RAPID = puck
                break

        rotation, forward_grip = puck_to_RAPID.check_collision(robtarget_pucks)
        rot = OpenCV_to_RAPID.z_degrees_to_quaternion(rotation)
        norbert.set_rapid_variable("gripper_angle", rotation)
        norbert.set_rapid_array("gripper_camera_offset", OpenCV_to_RAPID.gripper_camera_offset(rot))

        norbert.set_robtarget_translation("puck_target", puck_to_RAPID.get_xyz())
        norbert.set_rapid_variable("image_processed", "TRUE")  # Robot may move toward selected puck

        robtarget_pucks.remove(puck_to_RAPID)  # Remove puck so that it may be added to the list again later

        print('\nWhere should the puck be moved to? \nEnter x, y and z coordinates, '
              'or leave empty to move to middle of work area.\n')

        x = input("x: ")
        y = input("y: ")
        z = input("z: ")
        norbert.set_robtarget_translation("put_puck_target", [x, y, z])

        norbert.wait_for_rapid()  # Robot moves to close-up image position

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
