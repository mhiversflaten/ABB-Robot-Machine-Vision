#from config import config
import config_independent
from image_tools import ImageFunctions, camera_correction, QR_Reader
from RobotWebServices import RWS
import OpenCV_to_RAPID
import random
import threading

cam = config_independent.Camera()
cam.init()
cam.set_parameters()
cam.allocate_memory()
cam.capture_video()

# Show video feed in separate thread
cam_thread = threading.Thread(target=ImageFunctions.showVideo, args=(cam,), daemon=True)
cam_thread.start()

robtarget_pucks = []
all_pucks = []
puck_to_RAPID = 0

# Initialize robot communication, start motors, and execute RAPID program
norbert = RWS.RWS()
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
        8. Focus testing
        9. Exit
        """)

    userinput = int(input('\nWhat should RAPID do?: '))

    if userinput == 10000:
        from image_tools import QR_Reader
        import cv2
        gripper_height = norbert.get_gripper_height()
        img = ImageFunctions.capture_image(cam, gripper_height)
        img = QR_Reader.QR_Scanner_visualized(img)
        cv2.imwrite('Scanned_puck.png', img)


    if userinput == 1:
        print("Pick and place a single puck")
        norbert.set_rapid_variable("WPW", 1)
        norbert.wait_for_rapid()

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

        print('Which puck should be moved? Options: "', end='')
        print(*puck_numbers, sep='", "', end='"')
        pucknr = int(input(': '))

        for puck in robtarget_pucks:
            if puck.number == pucknr:
                puck_to_RAPID = puck
                break

        rot = OpenCV_to_RAPID.z_degrees_to_quaternion(0)
        #norbert.set_robtarget_rotation_quaternion("puck_target", rot)
        norbert.set_rapid_array("gripper_camera_offset", OpenCV_to_RAPID.gripper_camera_offset(rot))
        norbert.set_robtarget_translation("puck_target", puck_to_RAPID.get_xyz())
        norbert.set_rapid_variable("image_processed", "TRUE")

        robtarget_pucks.remove(puck_to_RAPID)

        print('\nWhere should the puck be moved to? \nEnter x, y and z coordinates, '
              'or leave empty to move to middle of work area.\n')

        x = input("x: ")
        y = input("y: ")
        z = input("z: ")
        norbert.set_robtarget_translation("put_puck_target", [x, y, z])

        norbert.wait_for_rapid()

        # Capture images until the puck is found again in the close-up image
        while not any(pucknr == x.number for x in robtarget_pucks):
            ImageFunctions.findPucks(cam, norbert, robtarget_pucks)

        for puck in robtarget_pucks:
            if puck.number == pucknr:
                puck_to_RAPID = puck
                break

        # rotation = puck_to_RAPID.check_collision(robtarget_pucks)
        rotation = 149
        norbert.set_rapid_variable("puck_angle", rotation)
        rot = OpenCV_to_RAPID.z_degrees_to_quaternion(rotation)
        norbert.set_rapid_array("gripper_camera_offset", OpenCV_to_RAPID.gripper_camera_offset(rot))
        #norbert.set_robtarget_rotation_quaternion("puck_target", rot)
        norbert.set_robtarget_translation("puck_target", puck_to_RAPID.get_xyz())
        norbert.set_rapid_variable("image_processed", "TRUE")

        robtarget_pucks.remove(puck_to_RAPID)
        print(robtarget_pucks)

    if userinput == 3:
        print("Stack pucks")
        norbert.set_rapid_variable("WPW", 3)
        norbert.wait_for_rapid()

        angle = 0
        while not robtarget_pucks:
            ImageFunctions.findPucks(cam, norbert, robtarget_pucks, number_of_images=5)
        print("Found pucks: ", end='')
        print(*robtarget_pucks, sep=', ')
        all_pucks = robtarget_pucks  # Permanent robtarget puck list
        for puck in robtarget_pucks:
            print("number: ", puck.number, "angle:", puck.angle)

        norbert.set_rapid_variable("length", len(robtarget_pucks))
        norbert.set_rapid_variable("image_processed", "TRUE")

        for _ in range(len(robtarget_pucks)):

            pucknr = min(int(x.number) for x in robtarget_pucks)

            for puck in robtarget_pucks:
                if puck.number == pucknr:
                    puck_to_RAPID = puck
                    break

            rot = OpenCV_to_RAPID.z_degrees_to_quaternion(0)

            norbert.set_rapid_variable("puck_angle", puck_to_RAPID.angle)
            norbert.set_robtarget_rotation_quaternion("puck_target", rot)
            norbert.set_rapid_array("gripper_camera_offset", OpenCV_to_RAPID.gripper_camera_offset(rot))
            norbert.set_robtarget_translation("puck_target", puck_to_RAPID.get_xyz())
            norbert.set_rapid_variable("image_processed", "TRUE")
            puck_to_RAPID.set_position([0, 150])

            robtarget_pucks.remove(puck_to_RAPID)

            norbert.wait_for_rapid()

            # Capture images until the puck is found again in the close-up image
            while not any(pucknr == x.number for x in robtarget_pucks):
                ImageFunctions.findPucks(cam, norbert, robtarget_pucks)

            pucknr = min(int(x.number) for x in robtarget_pucks)

            for puck in robtarget_pucks:
                if puck.number == pucknr:
                    puck_to_RAPID = puck
                    break

            rotation = puck_to_RAPID.check_collision(robtarget_pucks)
            rot = OpenCV_to_RAPID.z_degrees_to_quaternion(rotation)

            #norbert.set_rapid_variable("puck_angle", puck_to_RAPID.angle)
            norbert.set_robtarget_rotation_quaternion("puck_target", rot)
            norbert.set_rapid_array("gripper_camera_offset", OpenCV_to_RAPID.gripper_camera_offset(rot))
            norbert.set_robtarget_translation("puck_target", puck_to_RAPID.get_xyz())
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
        config_independent.repeatability_test = True

        i = 1
        # config_independent.number_of_loops = 0
        angle = 140
        # After two loops, the puck is picked up and placed at a random location
        while norbert.is_running():

            # Start Repeatability test CASE in RAPID
            norbert.set_rapid_variable("WPW", 6)
            norbert.wait_for_rapid()

            # Set a random target to place the puck in
            random_target = [random.randint(-50, 150), random.randint(-150, 150), 0]
            norbert.set_robtarget_translation("randomTarget", random_target)

            image_counter = 0
            while not robtarget_pucks:
                robtarget_pucks = ImageFunctions.findPucks(cam, norbert, robtarget_pucks)
                image_counter += 1
                if image_counter > 10:
                    robtarget_pucks.clear()
                    camera_correction.find_correct_exposure(cam, norbert)
                    cam.set_parameters()
                    image_counter = 0

            # Extract puck from list and send its position to RAPID
            puck_to_RAPID = robtarget_pucks[0]

            # Things that should only happen in one of the two loops should use an incremented variable and modulus
            if i % 2 == 0:
                config_independent.number_of_loops += 1
                print(config_independent.number_of_loops)
            rot = OpenCV_to_RAPID.z_degrees_to_quaternion(angle)
            print(rot)

            norbert.set_rapid_variable("puck_angle", angle)
            norbert.set_robtarget_rotation_quaternion("puck_target", rot)
            norbert.set_rapid_array("gripper_camera_offset", OpenCV_to_RAPID.gripper_camera_offset(rot))
            norbert.set_robtarget_translation("puck_target", puck_to_RAPID.get_xyz())
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
                norbert.set_robtarget_translation('gripper_target', targets[i])
                norbert.set_rapid_variable('WPW', 100)
                norbert.wait_for_rapid()

    elif userinput == 101:
        norbert.set_speeddata('vSpeed', 300)
        norbert.set_zonedata('zZone', 200)

    elif userinput == 103:
        norbert.set_rapid_variable("WPW", 103)
        norbert.wait_for_rapid()

        while not robtarget_pucks:
            ImageFunctions.findPucks(cam, norbert, robtarget_pucks, 195)

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

        norbert.set_robtarget_translation("puck_target", puck_to_RAPID.get_xyz())
        norbert.set_rapid_variable("image_processed", "TRUE")

        robtarget_pucks.remove(puck_to_RAPID)

        norbert.wait_for_rapid()
        ImageFunctions.findPucks(cam, norbert, robtarget_pucks, 160)

        for x in robtarget_pucks:
            if x.nr == whichPuck:
                puck_to_RAPID = x
                break

        norbert.set_robtarget_translation("puck_target", puck_to_RAPID.get_xyz())
        robtarget_pucks.clear()
        norbert.set_rapid_variable("image_processed", "TRUE")

    elif userinput == 6:
        camera_correction.find_correct_exposure(cam, norbert)

    elif userinput == 7:
        camera_correction.camera_adjustment(cam, norbert)

    elif userinput == 8:
        i = 0
        updated_z = 560
        while norbert.is_running() and updated_z > -50:
            updated_z = 550 - i*15
            i += 1
            # Start focus values test in RAPID
            norbert.set_robtarget_translation("focustarget", [0, 0, updated_z])
            norbert.set_rapid_variable("WPW", 7)
            norbert.wait_for_rapid()

            gripper_height = norbert.get_gripper_height()
            # Capture image
            ImageFunctions.capture_image(cam, gripper_height)

    elif userinput == 11:
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
            QR_Reader.QR_Scanner(img)

    elif userinput == 12:
        """Picking pucks from stacks"""



    elif userinput == 9:
        print("Exiting Python program and turning off robot motors")
        norbert.stop_RAPID()
        norbert.motors_off()

    elif userinput == 10:
        i = 0
        angle = 0
        # After two loops, the puck is picked up and placed at a random location
        while norbert.is_running():

            # Start Repeatability test CASE in RAPID
            norbert.set_rapid_variable("WPW", 9)
            norbert.wait_for_rapid()

            # Set a random target to place the puck in
            # random_target = [random.randint(-50, 150), random.randint(-200, -50), 0]  # Had (-150, 150)
            random_target = [-100, 150, 0]
            norbert.set_robtarget_translation("randomTarget", random_target)

            # Capture images until a puck is found
            while not robtarget_pucks:
                robtarget_pucks = ImageFunctions.findPucks(cam, norbert, robtarget_pucks)

            # Extract puck from list and send its position to RAPID
            puck_to_RAPID = robtarget_pucks[0]

            # Things that should only happen in one of the two loops should use an incremented variable and modulus
            """if i % 2 == 0:
                angle = random.randint(-100, 100)"""
            rot = OpenCV_to_RAPID.z_degrees_to_quaternion(angle)

            norbert.set_robtarget_rotation_quaternion("puck_target", rot)
            norbert.set_rapid_array("gripper_camera_offset", OpenCV_to_RAPID.gripper_camera_offset(rot))
            norbert.set_robtarget_translation("puck_target", puck_to_RAPID.get_xyz())
            norbert.set_rapid_variable("image_processed", "TRUE")
            print(puck_to_RAPID.get_xyz())

            # Remove the used puck from the list so it can be added once again next loop
            robtarget_pucks.remove(puck_to_RAPID)

            i += 1

cam.exit_camera()