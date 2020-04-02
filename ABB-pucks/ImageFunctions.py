import cv2
from QR_Reader import QR_Scanner, QR_Scanner_visualized
import config
from pyueye import ueye
import time
from pyueye_example_utils import ImageData, ImageBuffer
import OpenCV_to_RAPID


# TODO: Extend the program with threading, this will allow the camera to always stay active
#  and could give a live feed of what the camera sees while still maintaining control over robot.


def overviewImage():
    """Get the location and orientation of all pucks in the scene
    by grabbing several images with different threshold values."""

    while config.cap.isOpened():
        ret, frame = config.cap.read()  # Read image to np.array
        if ret:
            # Extracts position, orientation, which pucks were detected, and image with marked QR codes:
            if is_blurry(img=frame, threshold=80):
                return "failed"
            else:
                pos, img = QR_Scanner(img=frame)
                if not config.puckdict:
                    continue
                print("success")
                return "success"
            # break


def capture_image(cam, gripper_height):
    camera_height = gripper_height + 70  # Camera is placed 70mm above gripper
    # TODO: Find a curve that correlates distance from subject and focus value
    if camera_height > 300:
        nRet = ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_MANUAL_FOCUS,
                             config.focus_overview, ueye.sizeof(config.focus_overview))
    else:
        nRet = ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_MANUAL_FOCUS,
                             config.focus_closeup, ueye.sizeof(config.focus_closeup))

    #nRet = ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_ENABLE_AUTOFOCUS_ONCE, None, 0)

    # autofocus_status = ueye.INT(0)
    # ueye.is_Focus(cam.handle(), ueye.FOC_CMD_GET_AUTOFOCUS_STATUS, autofocus_status, ueye.sizeof(autofocus_status))
    img_buffer = ImageBuffer()  # Create image buffer
    #ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_ENABLE_AUTOFOCUS_ONCE, None, 0)
    time.sleep(0.5)
    # cam.freeze_video(True)  # Freeze video captures a single image

    nRet = ueye.is_WaitForNextImage(cam.handle(), 1000, img_buffer.mem_ptr, img_buffer.mem_id)
    img_data = ImageData(cam.handle(), img_buffer)
    array = img_data.as_1d_image()
    img_data.unlock()

    return array


def findPucks(cam, robot, robtarget_pucks, cam_comp=False):
    """Finds all pucks in the frame of the camera by capturing an image and scanning the image for QR codes.
    After the codes have been pinpointed, a series of transformations happen to finally create robtargets
    which can be sent to RobotWare."""
    temp_puck_list = []  # Temporary puck list

    trans, rot = robot.get_gripper_position()
    gripper_height = robot.get_gripper_height()

    cam_pos = OpenCV_to_RAPID.get_camera_position(trans=trans, rot=rot)

    image = capture_image(cam=cam, gripper_height=gripper_height)

    # Scan the image and return all QR code positions
    puck_list = QR_Scanner(image)

    # Check if the QR codes that were found have already been located previously.
    # If so, remove them from the temporary list.
    for puck in temp_puck_list:
        if any(puck == x for x in robtarget_pucks):
            puck_list.remove(puck)

    for puck in puck_list:
        OpenCV_to_RAPID.create_robtarget(gripper_height=gripper_height, gripper_rot=rot, cam_pos=cam_pos, puck=puck,
                                         cam_comp=cam_comp)
        robtarget_pucks.append(puck)

    return robtarget_pucks


def showVideo(cam):
    nRet = ueye.is_CaptureVideo(cam.handle(), ueye.IS_DONT_WAIT)
    img_buffer = ImageBuffer()
    img_data = ImageData(cam.handle(), img_buffer)
    while True:
        nRet = ueye.is_WaitForNextImage(cam.handle(), 1000, img_buffer.mem_ptr, img_buffer.mem_id)
        array = img_data.as_1d_image()
        #scanned_img = QR_Scanner_visualized(array)
        cv2.imshow("hei", array)
        img_data.unlock()
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


def is_blurry(img, threshold):
    laplacian_variance = cv2.Laplacian(img, cv2.CV_64F).var()
    print("Blur", laplacian_variance)
    if laplacian_variance > threshold:
        return False
    else:
        return True

