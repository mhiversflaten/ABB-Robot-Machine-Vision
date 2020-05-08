import cv2
from image_tools.QR_Reader import QR_Scanner, QR_Scanner_visualized
from pyueye import ueye
import time
from image_tools.pyueye_example_utils import ImageData, ImageBuffer
import OpenCV_to_RAPID


def capture_image(cam, gripper_height):
    """Captures a single image through PyuEye functions. Focus is manually adjusted depending on the height
    of the camera above the subject.
    """
    camera_height = gripper_height + 70  # Camera is placed 70mm above gripper
    # TODO: Find a curve that correlates distance from subject and focus value

    height_above_subject = gripper_height + 70 - 30  # -30 because one puck

    calculate_focus(cam, height_above_subject)

    #nRet = ueye.is_Focus(cam.hCam, ueye.FOC_CMD_SET_ENABLE_AUTOFOCUS_ONCE, None, 0)

    # TODO: For finding focus values for the function and case 8 in main.
    # Short pause before capturing image to ensure that the camera is still and focused
    """time.sleep(3)
    focus_value = ueye.UINT()
    ueye.is_Focus(cam.hCam, ueye.FOC_CMD_GET_MANUAL_FOCUS, focus_value, ueye.sizeof(focus_value))
    print(focus_value.value)

    focus_file = open('focus_file_XS.txt', 'a')

    focus_file.write("Camera Height: {0}, Focus Value: {1}\n".format(camera_height, focus_value.value))"""

    array = cam.get_image()

    return array


def calculate_focus(cam, height_above_subject):
    """This characteristic belongs to the IDS XS camera with serial code 4102885308.
    As stated by IDS themselves the characteristic is not robust and could vary between
    different cameras."""

    if height_above_subject >= 357.5:
        focus_value = 204
    elif 237 <= height_above_subject < 357.5:
        focus_value = 192
    elif 169 <= height_above_subject < 237:
        focus_value = 180
    elif 131.5 <= height_above_subject < 169:
        focus_value = 168
    elif 101.5 <= height_above_subject < 131.5:
        focus_value = 156
    elif 86.5 <= height_above_subject < 101.5:
        focus_value = 144
    elif 72 <= height_above_subject < 86.5:
        focus_value = 128
    elif 42.5 <= height_above_subject < 72:
        focus_value = 112
    else:
        print("Too close to subject. Focus value not found. Default value: 204")
        focus_value = 204

    focus_UINT = ueye.UINT(focus_value)
    ueye.is_Focus(cam.hCam, ueye.FOC_CMD_SET_MANUAL_FOCUS, focus_UINT, ueye.sizeof(focus_UINT))
    time.sleep(0.3)


def findPucks(cam, robot, robtarget_pucks, cam_comp=False, number_of_images=1):
    """Finds all pucks in the frame of the camera by capturing an image and scanning the image for QR codes.
    After the codes have been pinpointed, a series of transformations happen to finally create robtargets
    which can be sent to RobotWare."""

    trans, rot = robot.get_gripper_position()
    gripper_height = robot.get_gripper_height()

    cam_pos = OpenCV_to_RAPID.get_camera_position(trans=trans, rot=rot)

    for _ in range(number_of_images):
        image = capture_image(cam=cam, gripper_height=gripper_height)

        # Scan the image_tools and return all QR code positions
        temp_puck_list = QR_Scanner(image)

        # Check if the QR codes that were found have already been located previously.
        # If so, remove them from the temporary list.
        for puck in robtarget_pucks:
            if any(puck == x for x in temp_puck_list):
                temp_puck_list.remove(puck)

        for puck in temp_puck_list:
            puck = OpenCV_to_RAPID.create_robtarget(gripper_height=gripper_height, gripper_rot=rot, cam_pos=cam_pos,
                                                    puck=puck, cam_comp=cam_comp)
            robtarget_pucks.append(puck)

    return robtarget_pucks


def showVideo(cam):
    while True:
        array = cam.get_image()
        array = QR_Scanner_visualized(array)
        # array = cv2.resize(array,(0,0),fx=0.5, fy=0.5)
        cv2.imshow("Continuous video display", array)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
