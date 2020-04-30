import configparser
import time
from image_tools.QR_Reader import QR_Scanner
from pyueye import ueye
from numpy import median
from image_tools import ImageFunctions
from RobotWare import RAPID

norbert = RAPID.RAPID()
norbert.request_mastership()
norbert.start_RAPID()  # NB! Starts RAPID execution from main
norbert.wait_for_rapid()
norbert.stop_RAPID()
norbert.motors_off()

# List with exposure values
exposure_values = []
# Exposure range (in ms)
exposure_low = 1
exposure_high = 66

# Initialize camera
from config import config

cam = config.cam

gain = ueye.INT(10)
#ueye.is_SetHardwareGain(cam.handle(), gain, ueye.IS_IGNORE_PARAMETER, ueye.IS_IGNORE_PARAMETER,
                        #ueye.IS_IGNORE_PARAMETER)

# Increment
increment = 2
# Loop from lowest possible exposure to highest possible exposure, incremented by 2 (ms)
for exposure in range(exposure_low, exposure_high, increment):
    # Set new exposure
    newExposure = ueye.DOUBLE(exposure)
    ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, newExposure, ueye.sizeof(newExposure))
    #time.sleep(0.05)
    img = ImageFunctions.capture_image(cam=cam, gripper_height=500)
    puck_list = QR_Scanner(img)
    print(puck_list)
    # Checking exposure
    d = ueye.DOUBLE()
    retVal = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, d, 8)
    if retVal == ueye.IS_SUCCESS:
        print('Currently set exposure time %8.3f ms' % d)
    # Position returns as None if no QR-code is found
    if puck_list:
        exposure_values.append(exposure)

exposure = str(median(exposure_values))

config = configparser.ConfigParser()
config.read('cam_adjustments.ini')
cfgfile = open('cam_adjustments.ini', 'w')

# Updating the value for exposure
config.set('EXPOSURE', 'exposure', exposure)

config.write(cfgfile)
cfgfile.close()
