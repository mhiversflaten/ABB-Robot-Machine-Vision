import cv2
from pyueye import ueye
from image_tools.pyueye_example_camera import Camera
from image_tools.pyueye_example_utils import ImageData, ImageBuffer
import time
import numpy as np

# Initialize camera
cam = Camera()
cam.init()

nRet = ueye.is_ResetToDefault(cam.handle())

# Change the format to 1280x960
formatID = ueye.UINT(8)
nRet = ueye.is_ImageFormat(cam.handle(), ueye.IMGFRMT_CMD_SET_FORMAT, formatID, ueye.sizeof(formatID))

cam.alloc()  # Allocate image_tools memory

# Disable auto exposure
dblEnable = ueye.DOUBLE(0)
dblDummy = ueye.DOUBLE(0)
ueye.is_SetAutoParameter(cam.handle(), ueye.IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER, dblEnable, dblDummy)

newExposure = ueye.DOUBLE(30)
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, newExposure, ueye.sizeof(newExposure))

ueye.is_Focus(cam.handle(), ueye.FOC_CMD_SET_DISABLE_AUTOFOCUS, None, 0)  # Disable autofocus

focus_overview = ueye.INT(205)  # Focus value for overview image_tools (taken from 570mm above table)
focus_closeup = ueye.INT(144)  # Focus value for closeup image_tools (taken from 190mm above table)


"""
exp_min = ueye.DOUBLE()
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MIN, exp_min, ueye.sizeof(exp_min))
exp_max = ueye.DOUBLE()
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MAX, exp_max, ueye.sizeof(exp_max))
print(exp_min, exp_max)
exp_def = ueye.DOUBLE()
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_DEFAULT, exp_def, ueye.sizeof(exp_def))
print(exp_def)

disable = ueye.DOUBLE(0)
dummy = ueye.DOUBLE(0)
ret = ueye.is_SetAutoParameter(cam.handle(), ueye.IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER, disable, dummy)
exp_val = ueye.DOUBLE(10.0)
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, exp_val, ueye.sizeof(exp_val))

exp_def = ueye.DOUBLE()
ret = ueye.is_Exposure(cam.handle(), ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, exp_def, ueye.sizeof(exp_def))
print("set exp to", exp_def)"""
