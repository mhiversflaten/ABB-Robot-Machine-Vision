import cv2
from pyueye import ueye

from image_tools.pyueye_example_camera import Camera
from image_tools.pyueye_example_utils import ImageBuffer, ImageData

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

nRet = ueye.is_CaptureVideo(cam.handle(), ueye.IS_WAIT)


while True:
    img_buffer = ImageBuffer()
    nRet = ueye.is_WaitForNextImage(cam.handle(), 1000, img_buffer.mem_ptr, img_buffer.mem_id)
    img_data = ImageData(cam.handle(), img_buffer)
    array = img_data.as_1d_image()
    # scanned_img = QR_Scanner_visualized(array)
    cv2.imshow("hei", array)
    img_data.unlock()
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break