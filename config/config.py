from pyueye import ueye
from image_tools.pyueye_example_camera import Camera
import configparser

# Initialize camera
cam = Camera()
cam.init()

nRet = ueye.is_ResetToDefault(cam.handle())

# Change the format to 1280x960
formatID = ueye.UINT(8)
nRet = ueye.is_ImageFormat(cam.handle(), ueye.IMGFRMT_CMD_SET_FORMAT, formatID, ueye.sizeof(formatID))

cam.alloc()  # Allocate image memory

# Disable auto exposure
dblEnable = ueye.DOUBLE(0)
dblDummy = ueye.DOUBLE(0)
ueye.is_SetAutoParameter(cam.handle(), ueye.IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER, dblEnable, dblDummy)


config = configparser.ConfigParser()
config.read('image_tools/cam_adjustments.ini')

exposure = float(config['EXPOSURE']['exposure'])

newExposure = ueye.DOUBLE(exposure)
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, newExposure, ueye.sizeof(newExposure))

ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_DISABLE_AUTOFOCUS, None, 0)  # Disable autofocus

focus_overview = ueye.INT(205)  # Focus value for overview image (taken from 570mm above table)
focus_closeup = ueye.INT(144)  # Focus value for closeup image (taken from 190mm above table)
