import cv2
import config_independent
from image_tools.QR_Reader import QR_Scanner, QR_Scanner_visualized
from pyueye import ueye
import time
import OpenCV_to_RAPID


def capture_image(cam, gripper_height):
    """Captures a single image through PyuEye functions.
    Focus is manually adjusted depending on the working distance.
    """
    camera_height = gripper_height + 70  # Camera is placed 70mm above gripper
    working_distance = camera_height - 30  # -30 because one puck

    calculate_focus(cam, working_distance)

    # Trigger autofocus once (use instead of calculate_focus if needed):
    # nRet = ueye.is_Focus(cam.hCam, ueye.FOC_CMD_SET_ENABLE_AUTOFOCUS_ONCE, None, 0)

    array = cam.get_image()

    return array


def calculate_focus(cam, working_distance):
    """This characteristic belongs to the IDS XS camera with serial code 4102885308.
    As stated by IDS themselves the characteristic is not robust and could vary between
    different cameras.
    The characteristic was made based on images up to a working distance of 620mm.
    """
    if working_distance >= 357.5:
        focus_value = 204
    elif 237 <= working_distance < 357.5:
        focus_value = 192
    elif 169 <= working_distance < 237:
        focus_value = 180
    elif 131.5 <= working_distance < 169:
        focus_value = 168
    elif 101.5 <= working_distance < 131.5:
        focus_value = 156
    elif 86.5 <= working_distance < 101.5:
        focus_value = 144
    elif 72 <= working_distance < 86.5:
        focus_value = 128
    elif 42.5 <= working_distance < 72:
        focus_value = 112
    else:
        print("Too close to subject. Focus value not found. Default value: 204")
        focus_value = 204

    # Set the correct focus value
    focus_UINT = ueye.UINT(focus_value)
    ueye.is_Focus(cam.hCam, ueye.FOC_CMD_SET_MANUAL_FOCUS, focus_UINT, ueye.sizeof(focus_UINT))
    time.sleep(0.3)


def approximate_stack(qr_width, gripper_height):

    if qr_width >= 400:
        focus_value = 204
    elif 237 <= qr_width < 357.5:
        focus_value = 192
    elif 169 <= qr_width < 237:
        focus_value = 180
    elif 131.5 <= qr_width < 169:
        focus_value = 168
    elif 101.5 <= qr_width < 131.5:
        focus_value = 156
    elif 86.5 <= qr_width < 101.5:
        focus_value = 144
    elif 72 <= qr_width < 86.5:
        focus_value = 128
    elif 42.5 <= qr_width < 72:
        focus_value = 112
    else:
        print("Too close to subject. Focus value not found. Default value: 204")
        focus_value = 204



    # Create robtargets for every new puck
    for puck in temp_puck_list:
        puck = OpenCV_to_RAPID.create_robtarget(gripper_height=gripper_height, gripper_rot=rot, cam_pos=cam_pos,
                                                image=image, puck=puck, cam_comp=cam_comp)
        robtarget_pucks.append(puck)



def findPucks(cam, robot, robtarget_pucks, cam_comp=False, number_of_images=1):
    """Finds all pucks in the frame of the camera by capturing an image and scanning the image for QR codes.
    After the codes have been pinpointed, a series of transformations happen to finally create robtargets
    which can be sent to RobotWebServices.
    """

    trans, rot = robot.get_gripper_position()
    gripper_height = robot.get_gripper_height()

    cam_pos = OpenCV_to_RAPID.get_camera_position(trans=trans, rot=rot)

    for _ in range(number_of_images):
        image = capture_image(cam=cam, gripper_height=gripper_height)

        # Scan the image and return all QR code positions
        temp_puck_list = QR_Scanner(image)

        # Check if the QR codes that were found have already been located previously.
        # If so, remove them from the temporary list.
        for puck in robtarget_pucks:
            if any(puck == x for x in temp_puck_list):
                temp_puck_list.remove(puck)

        # Create robtargets for every new puck
        for puck in temp_puck_list:
            puck = OpenCV_to_RAPID.create_robtarget(gripper_height=gripper_height, gripper_rot=rot, cam_pos=cam_pos,
                                                    image=image, puck=puck, cam_comp=cam_comp)
            robtarget_pucks.append(puck)

    return robtarget_pucks


def showVideo(cam):
    """Continuously displays the robot's view in an OpenCV imshow window.
    """
    while True:
        if config_independent.repeatability_test:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10, 50)
            fontScale = 1
            fontColor = (255, 255, 255)
            lineType = 2

            cv2.putText(array, 'Number of loops: ' + str(config_independent.number_of_loops),
                        bottomLeftCornerOfText,
                        font,
                        fontScale,
                        fontColor,
                        lineType)

        array = cam.get_image()
        array = QR_Scanner_visualized(array)
        # array = cv2.resize(array,(0,0),fx=0.5, fy=0.5)
        cv2.imshow("Continuous video display", array)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
