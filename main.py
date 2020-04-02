from config import config
from image_tools import ImageFunctions
from RobotWare import RAPID
import random
import threading

# Show video feed in separate thread
cam_thread = threading.Thread(target=ImageFunctions.showVideo, args=(config.cam,), daemon=True)
cam_thread.start()


robtarget_pucks = []
puck_to_RAPID = 0

# Initialize robot communication, start motors, and execute RAPID program
norbert = RAPID.RAPID()
norbert.request_rmmp()
norbert.start_RAPID()  # NB! Starts RAPID execution from main
norbert.wait_for_rapid()

# Run script while RAPID execution is running
while norbert.is_running():
    print("""
        1. Image from above
        2. Move puck to middle
        3. Stack pucks
        4. Rotate puck
        5. Exit
        6. Repeatability test""")

    userinput = int(input('\nWhat should RAPID do?: '))

    if userinput == 3:
        print("Stack pucks")
        norbert.set_rapid_variable("WPW", 3)
        norbert.wait_for_rapid()

        while not robtarget_pucks:
            ImageFunctions.findPucks(config.cam, norbert, robtarget_pucks, 195)
        print(robtarget_pucks)

        for _ in range(len(robtarget_pucks)):

            pucknr = min(int(x.nr) for x in robtarget_pucks)

            for x in robtarget_pucks:
                if x.nr == pucknr:
                    puck_to_RAPID = x
                    break

            norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
            norbert.set_rapid_variable("puck_angle", puck_to_RAPID.get_puckang())
            norbert.set_rapid_variable("image_processed", "TRUE")

            robtarget_pucks.remove(puck_to_RAPID)

            norbert.wait_for_rapid()

            ImageFunctions.findPucks(config.cam, norbert, robtarget_pucks, 160)

            pucknr = min(int(x.nr) for x in robtarget_pucks)

            for x in robtarget_pucks:
                if x.nr == pucknr:
                    puck_to_RAPID = x
                    break

            norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
            norbert.set_rapid_variable("image_processed", "TRUE")

            robtarget_pucks.remove(puck_to_RAPID)

            norbert.wait_for_rapid()

    elif userinput == 6:
        """The repeatability test uses only one puck in the work area, which is to be found, 
        picked up, and placed at a random location. Once this is done, the robot returns to its 
        original position and repeats the process, without prior knowledge of the puck's location."""
        print("Repeatability test started")
        # TODO: Change WPW and randomTarget only every other loop

        # After two loops, the puck is picked up and placed at a random location
        while norbert.is_running():

            # Start Repeatability test CASE in RAPID
            norbert.set_rapid_variable("WPW", 6)
            norbert.wait_for_rapid()

            # Set a random target to place the puck in
            random_target = [random.randint(-50, 150), random.randint(-150, 150), 0]
            norbert.set_robtarget_variables("randomTarget", random_target)

            # Capture images until a puck is found
            while not robtarget_pucks:
                ImageFunctions.findPucks(config.cam, norbert, robtarget_pucks)

            # Extract puck from list and send its position to RAPID
            puck_to_RAPID = robtarget_pucks[0]
            norbert.set_robtarget_variables("puck_target", puck_to_RAPID.get_xyz())
            norbert.set_rapid_variable("image_processed", "TRUE")

            # Remove the used puck from the list so it can be added once again next loop
            robtarget_pucks.remove(puck_to_RAPID)

    elif userinput == 105:
        new_speed = int(input("Enter new speed data:\n"))
        norbert.set_rapid_variable("vSpeed", new_speed)

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

    elif userinput == 5:
        print("Exiting Python program and turning off robot motors")
        norbert.stop_RAPID()
        norbert.motors_off()


"testing string"
