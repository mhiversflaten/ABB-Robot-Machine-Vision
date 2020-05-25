import image_tools.ImageFunctions
from image_tools import ImageFunctions, camera_correction, Camera
from RobotWebServices import RWS
import OpenCV_to_RAPID
import random
import threading

# Initialize communication with Norbert, start motors, and execute RAPID program
norbert = RWS.RWS('http://152.94.0.38')  # Norbert's IP address
norbert.request_mastership()
norbert.start_RAPID()  # NB! Starts RAPID execution from main

# Initialize uEye XS camera
cam = Camera.Camera()
cam.init()
cam.set_parameters()
cam.allocate_memory()
cam.capture_video()

# Show video feed in separate thread
cam_thread = threading.Thread(target=ImageFunctions.showVideo, args=(cam,), daemon=True)
cam_thread.start()

robtarget_pucks = []
puck_to_RAPID = 0
angle = 0

norbert.wait_for_rapid()  # Wait for robot to be in standard position (overview)

while norbert.is_running():  # Run script while RAPID execution is running
    print("""
        Choose what to do:
        1: Pick and place a single puck
        2: Stack pucks
        3: Repeatability test
        4: Find correct exposure
        5: Camera adjustment
        6: Focus testing
        7: Change speeddata
        8: Change zonedata
        9: Change speed ratio 
        10: QR Width
        11: Picking pucks from stacks
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
        norbert.send_puck(puck_to_RAPID.get_xyz(), puck_to_RAPID.angle, rotation)

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

        rotation, forward_grip = puck_to_RAPID.check_collision(robtarget_pucks)
        norbert.send_puck(puck_to_RAPID.get_xyz(), puck_to_RAPID.angle, rotation, forward_grip)

        norbert.set_rapid_variable("image_processed", "TRUE")  # Robot may pick and place selected puck

        robtarget_pucks.remove(puck_to_RAPID)  # Remove puck so that it may be added to the list again later

    elif userinput == 2:
        """
        Stack all visible pucks in the work area. 
        Starts with the lowest numbered puck and stacks them in ascending order.
        Stack location can be set in RAPID script (origin is default).
        Uses collision avoidance when picking up pucks.
        """

        print("Stack pucks")
        norbert.set_rapid_variable("WPW", 3)
        norbert.wait_for_rapid()  # Robot goes to overview position

        # Capture X amount of images to ensure all pucks are found
        while not robtarget_pucks:
            ImageFunctions.findPucks(cam, norbert, robtarget_pucks, number_of_images=5)

        print("Found pucks: ", end='')
        print(*robtarget_pucks, sep=', ')

        for puck in robtarget_pucks:
            print("number:", puck.number, "angle:", puck.angle)
            print(f"{puck}; Position: {puck.position}, Angle: {puck.angle}, Height: {puck.height}")

        # Tell RAPID how many pucks were found
        norbert.set_rapid_variable("length", len(robtarget_pucks))
        norbert.set_rapid_variable("image_processed", "TRUE")  # Start the for-loop in RAPID

        for _ in range(len(robtarget_pucks)):

            pucknr = min(int(x.number) for x in robtarget_pucks)  # Find the lowest numbered puck

            # Extract the selected puck from the puck list -> puck_to_RAPID
            for puck in robtarget_pucks:
                if puck.number == pucknr:
                    puck_to_RAPID = puck
                    break

            rotation, forward_grip = puck_to_RAPID.check_collision(robtarget_pucks)
            norbert.send_puck(puck_to_RAPID.get_xyz(), puck_to_RAPID.angle, rotation)

            norbert.set_rapid_variable("image_processed", "TRUE")

            robtarget_pucks.remove(puck_to_RAPID)  # Remove puck so that it may be added to the list again later

            norbert.wait_for_rapid()  # Robot moves to close-up image position

            # Capture images until the puck is found again in the close-up image
            while not any(pucknr == x.number for x in robtarget_pucks):
                ImageFunctions.findPucks(cam, norbert, robtarget_pucks)

            # Extract the selected puck from the puck list -> puck_to_RAPID
            for puck in robtarget_pucks:
                if puck.number == pucknr:
                    puck_to_RAPID = puck
                    break

            rotation, forward_grip = puck_to_RAPID.check_collision(robtarget_pucks)
            norbert.send_puck(puck_to_RAPID.get_xyz(), puck_to_RAPID.angle, rotation, forward_grip)

            norbert.set_rapid_variable("image_processed", "TRUE")

            robtarget_pucks.remove(puck_to_RAPID)  # Remove the puck from the list as we're done with it

            norbert.wait_for_rapid()  # Robot may pick and place selected puck

    elif userinput == 3:
        """
        The repeatability test uses only one puck in the work area, which is to be found, 
        picked up, and placed at a random location. Once this is done, the robot returns to its 
        original position and repeats the process, without prior knowledge of the puck's location.
        """

        print("Repeatability test started")
        # TODO: Change WPW and randomTarget only every other loop
        Camera.repeatability_test = True

        i = 1
        # config_independent.number_of_loops = 0
        # After two loops, the puck is picked up and placed at a random location
        while norbert.is_running():

            # Start Repeatability test CASE in RAPID
            norbert.set_rapid_variable("WPW", 6)
            # Robot goes to overview position and close-up image position every other loop:
            norbert.wait_for_rapid()

            # Set a random target to place the puck in
            random_target = [random.randint(-50, 150), random.randint(-150, 150), 0]
            norbert.set_robtarget_translation("randomTarget", random_target)

            # Take up to 10 images of the work area
            image_counter = 0
            while not robtarget_pucks:
                robtarget_pucks = ImageFunctions.findPucks(cam, norbert, robtarget_pucks)
                image_counter += 1
                if image_counter > 10:
                    robtarget_pucks.clear()
                    # If pucks are not found, try to adjust exposure value
                    camera_correction.find_correct_exposure(cam, norbert)
                    image_counter = 0

            # Extract puck from list and send its position to RAPID
            puck_to_RAPID = robtarget_pucks[0]

            # Things that should only happen in one of the two loops should use an incremented variable and modulus
            if i % 2 == 0:
                # Increment number of loops for video display
                Camera.number_of_loops += 1
                print(Camera.number_of_loops)

            norbert.send_puck(puck_to_RAPID.get_xyz(), puck_to_RAPID.angle)

            norbert.set_rapid_variable("image_processed", "TRUE")

            # Remove the used puck from the list so it may be added once again next loop
            robtarget_pucks.remove(puck_to_RAPID)

            i += 1

    elif userinput == 4:
        camera_correction.find_correct_exposure(cam, norbert)

    elif userinput == 5:
        camera_correction.camera_adjustment(cam, norbert)

    elif userinput == 6:
        """Focus testing"""
        i = 0
        updated_z = 560
        while norbert.is_running() and updated_z > -50:
            updated_z = 550 - i * 15
            i += 1
            # Start focus values test in RAPID
            norbert.set_robtarget_translation("focustarget", [0, 0, updated_z])
            norbert.set_rapid_variable("WPW", 7)
            norbert.wait_for_rapid()

            gripper_height = norbert.get_gripper_height()
            # Capture image
            ImageFunctions.capture_image(cam, gripper_height)

    elif userinput == 7:
        """Changes speeddata of vSpeed in RAPID"""

        new_speed = int(input("Enter new speed data:"))
        norbert.set_speeddata('vSpeed', new_speed)

    elif userinput == 8:
        """Changes zonedata of zZone in RAPID"""

        print("Enter new zone data.")
        print("Choices: fine, 0, 1, 5, 10, 20, 30, 40, 50, 60, 80, 100, 150, 200")
        new_zonedata = input()

        if new_zonedata != 'fine':
            new_zonedata = int(new_zonedata)

        norbert.set_zonedata('zZone', new_zonedata)

    elif userinput == 9:
        """Change speed ratio of the robot controller"""

        new_speed_ratio = int(input("Enter new speed ratio:"))

        norbert.set_speed_ratio(new_speed_ratio)

    elif userinput == 10:
        """Find all corner distances (px) for the QR-codes with different gripper height"""

        i = 0
        updated_z = 60  # Starting at gripper height
        while norbert.is_running() and updated_z < 500:
            updated_z = 60 + i * 5
            print(updated_z)
            i += 1
            # Start focus values test in RAPID (using focustarget because it is already in RAPID program
            norbert.set_robtarget_translation("focustarget", [0, 0, updated_z])
            norbert.set_rapid_variable("WPW", 7)
            norbert.wait_for_rapid()

            gripper_height = norbert.get_gripper_height()
            # Capture image
            img = ImageFunctions.capture_image(cam, gripper_height)
            image_tools.ImageFunctions.QR_Scanner(img)

    elif userinput == 0:
        print("Exiting Python program and turning off robot motors")
        norbert.stop_RAPID()
        norbert.motors_off()

    else:
        print("The chosen option is not valid. Try again.")
        continue

cam.exit_camera()