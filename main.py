from config import config
from image_tools import ImageFunctions, camera_correction
from RobotWare import RAPID
import OpenCV_to_RAPID
import random
import threading

# Show video feed in separate thread
#cam_thread = threading.Thread(target=ImageFunctions.showVideo, args=(config.cam,), daemon=True)
#cam_thread.start()

robtarget_pucks = []
puck_to_RAPID = 0

# Initialize robot communication, start motors, and execute RAPID program
norbert = RAPID.RAPID()
norbert.request_mastership()
norbert.start_RAPID()  # NB! Starts RAPID execution from main
norbert.wait_for_rapid()

# Run script while RAPID execution is running
while norbert.is_running():
    print("""
        Choose what to do:
        1. Image from above
        2. Move puck to middle
        3. Stack pucks
        4. Rotate puck
        5. Repeatability test
        6. Find correct exposure
        7. Camera adjustment
        8. Exit
        """)

    userinput = int(input('\nWhat should RAPID do?: '))

    if userinput == 1:
        print("Pick and place a single puck")
        norbert.set_rapid_variable("WPW", 1)
        norbert.wait_for_rapid()

        robtarget_pucks = ImageFunctions.findPucks(config.cam, norbert, robtarget_pucks, number_of_images=5)

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

        print('Which puck should be moved? Options: "', end='')
        print(*puck_numbers, sep='", "', end='"')
        pucknr = int(input(': '))

        for puck in robtarget_pucks:
            if puck.number == pucknr:
                puck_to_RAPID = puck
                break

        norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
        norbert.set_rapid_variable("image_processed", "TRUE")

        robtarget_pucks.remove(puck_to_RAPID)

        print('\nWhere should the puck be moved to? \n Enter x, y and z coordinates, '
              'or leave empty to move to middle of work area.\n')

        x = input("x: ")
        y = input("y: ")
        z = input("z: ")
        norbert.set_robtarget_variables("put_puck_target", [x, y, z])

        norbert.wait_for_rapid()

        ImageFunctions.findPucks(config.cam, norbert, robtarget_pucks)

        for puck in robtarget_pucks:
            if puck.number == pucknr:
                puck_to_RAPID = puck
                break

        rot = OpenCV_to_RAPID.z_degrees_to_quaternion(0)
        norbert.set_rapid_array("gripper_camera_offset", OpenCV_to_RAPID.gripper_camera_offset(rot))

        norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
        norbert.set_rapid_variable("image_processed", "TRUE")

        robtarget_pucks.remove(puck_to_RAPID)
        print(robtarget_pucks)

    if userinput == 3:
        print("Stack pucks")
        norbert.set_rapid_variable("WPW", 3)
        norbert.wait_for_rapid()

        while not robtarget_pucks:
            ImageFunctions.findPucks(config.cam, norbert, robtarget_pucks)
        print("Found pucks: ", end='')
        print(*robtarget_pucks, sep=', ')
        for puck in robtarget_pucks:
            print("number: ", puck.number, "angle:", puck.angle)

        for _ in range(len(robtarget_pucks)):

            pucknr = min(int(x.number) for x in robtarget_pucks)

            for puck in robtarget_pucks:
                if puck.number == pucknr:
                    puck_to_RAPID = puck
                    break

            norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
            norbert.set_rapid_variable("image_processed", "TRUE")

            robtarget_pucks.remove(puck_to_RAPID)

            norbert.wait_for_rapid()

            ImageFunctions.findPucks(config.cam, norbert, robtarget_pucks)

            pucknr = min(int(x.number) for x in robtarget_pucks)

            for puck in robtarget_pucks:
                if puck.number == pucknr:
                    puck_to_RAPID = puck
                    break

            norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
            norbert.set_rapid_variable("image_processed", "TRUE")

            robtarget_pucks.remove(puck_to_RAPID)

            norbert.wait_for_rapid()

    elif userinput == 5:
        """The repeatability test uses only one puck in the work area, which is to be found, 
        picked up, and placed at a random location. Once this is done, the robot returns to its 
        original position and repeats the process, without prior knowledge of the puck's location.
        """
        print("Repeatability test started")
        # TODO: Change WPW and randomTarget only every other loop

        i = 0
        angle = 0
        # After two loops, the puck is picked up and placed at a random location
        while norbert.is_running():

            # Start Repeatability test CASE in RAPID
            norbert.set_rapid_variable("WPW", 6)
            norbert.wait_for_rapid()

            # Set a random target to place the puck in
            random_target = [random.randint(-50, 150), random.randint(-200, -50), 0]  # Had (-150, 150)
            norbert.set_robtarget_variables("randomTarget", random_target)

            # Capture images until a puck is found
            while not robtarget_pucks:
                robtarget_pucks = ImageFunctions.findPucks(config.cam, norbert, robtarget_pucks)

            # Extract puck from list and send its position to RAPID
            puck_to_RAPID = robtarget_pucks[0]

            # Things that should only happen in one of the two loops should use an incremented variable and modulus
            if i % 2 == 0:
                angle = random.randint(-100, 100)
            rot = OpenCV_to_RAPID.z_degrees_to_quaternion(angle)

            norbert.set_robtarget_rotation_quaternion("puck_target", rot)
            norbert.set_rapid_array("gripper_camera_offset", OpenCV_to_RAPID.gripper_camera_offset(rot))
            norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
            norbert.set_rapid_variable("image_processed", "TRUE")

            # Remove the used puck from the list so it can be added once again next loop
            robtarget_pucks.remove(puck_to_RAPID)

            i += 1

    elif userinput == 105:
        new_speed = int(input("Enter new speed data:\n"))
        norbert.set_speeddata('vSpeed', new_speed)

    elif userinput == 100:
        targets = [[100, 100, 100], [-100, 100, 100], [-100, -100, 100], [100, -100, 100]]
        while True:
            for i in range(len(targets)):
                norbert.set_robtarget_variables('gripper_target', targets[i])
                norbert.set_rapid_variable('WPW', 100)
                norbert.wait_for_rapid()

    elif userinput == 101:
        norbert.set_speeddata('vSpeed', 300)
        norbert.set_zonedata('zZone', 200)

    elif userinput == 103:
        norbert.set_rapid_variable("WPW", 103)
        norbert.wait_for_rapid()

        while not robtarget_pucks:
            ImageFunctions.findPucks(config.cam, norbert, robtarget_pucks, 195)

        puck_to_RAPID = robtarget_pucks[0]
        whichPuck = 3
        """while not puck_to_RAPID:
            whichPuck = input("Which puck do you wish to move?")
            for x in robtarget_pucks:
                if x.nr == whichPuck:
                    puck_to_RAPID = x
                    break
            else:
                print("The selected puck has not been detected! Please enter another number.\n")
                continue
            break"""

        norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
        norbert.set_rapid_variable("image_processed", "TRUE")

        robtarget_pucks.remove(puck_to_RAPID)

        norbert.wait_for_rapid()
        ImageFunctions.findPucks(config.cam, norbert, robtarget_pucks, 160)

        for x in robtarget_pucks:
            if x.nr == whichPuck:
                puck_to_RAPID = x
                break

        norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
        robtarget_pucks.clear()
        norbert.set_rapid_variable("image_processed", "TRUE")

    elif userinput == 6:
        camera_correction.find_correct_exposure(config.cam, norbert)

    elif userinput == 7:
        camera_correction.camera_adjustment(config.cam, norbert)

    elif userinput == 8:
        print("Exiting Python program and turning off robot motors")
        norbert.stop_RAPID()
        norbert.motors_off()
