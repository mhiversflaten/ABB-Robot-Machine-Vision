from RWS-UiS import RWS
from image_tools import ImageFunctions, Camera
import cv2

print(cv2.__version__)  # Check that OpenCV is installed

# Initialize communication with Norbert, start motors, and execute RAPID program
robot = RWS.RWS('http://152.94.0.38')  # Norbert's IP address
robot.request_mastership()
robot.start_RAPID()  # NB! Starts RAPID execution from main

# Initialize uEye XS camera
cam = Camera.Camera()
cam.init()
cam.set_parameters(disable_exposure=False)
cam.allocate_memory()
cam.capture_video()

robtarget_pucks = []
puck_to_RAPID = 0

robot.wait_for_rapid()  # Wait for robot to be in standard position (overview)

robtarget_pucks = ImageFunctions.findPucks(cam, robot, robtarget_pucks)

puck_to_RAPID = robtarget_pucks[0]

robot.set_robtarget_translation("puck_target", puck_to_RAPID.get_xyz())
robot.set_rapid_variable("image_processed", "TRUE")

