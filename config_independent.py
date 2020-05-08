from pyueye import ueye
import numpy as np
import cv2


class Camera:

    def __init__(self):
        self.hCam = ueye.HIDS(0)
        self.sInfo = ueye.SENSORINFO()
        self.cInfo = ueye.CAMINFO()
        self.pcImageMemory = ueye.c_mem_p()
        self.MemID = ueye.int()
        self.rectAOI = ueye.IS_RECT()
        self.pitch = ueye.INT()
        self.nBitsPerPixel = ueye.INT(32)  # 32 bits for color camera
        self.channels = 3  # 3: channels for color mode(RGB); take 1 channel for monochrome
        self.m_nColorMode = ueye.IS_CM_BGRA8_PACKED  # RGB32
        self.bytes_per_pixel = int(self.nBitsPerPixel / 8)

    def init(self):
        # Starts the driver and establishes the connection to the camera
        nRet = ueye.is_InitCamera(self.hCam, None)
        if nRet != ueye.IS_SUCCESS:
            print("is_InitCamera ERROR")

        nRet = ueye.is_ResetToDefault(self.hCam)
        if nRet != ueye.IS_SUCCESS:
            print("is_ResetToDefault ERROR")

    def set_parameters(self):
        # FormatID = ueye.UINT(8): Change image format to 1280x960
        # FormatID = ueye.UINT(5): Change image format to 2048x1536
        formatID = ueye.UINT(8)
        nRet = ueye.is_ImageFormat(self.hCam, ueye.IMGFRMT_CMD_SET_FORMAT, formatID, ueye.sizeof(formatID))

        # Disable auto exposure
        dblEnable = ueye.DOUBLE(0)
        dblDummy = ueye.DOUBLE(0)
        ueye.is_SetAutoParameter(self.hCam, ueye.IS_SET_ENABLE_AUTO_SENSOR_GAIN_SHUTTER, dblEnable, dblDummy)

        # Disable autofocus
        ueye.is_Focus(self.hCam, ueye.FOC_CMD_SET_DISABLE_AUTOFOCUS, None, 0)

    def allocate_memory(self):
        nRet = ueye.is_AOI(self.hCam, ueye.IS_AOI_IMAGE_GET_AOI, self.rectAOI, ueye.sizeof(self.rectAOI))
        if nRet != ueye.IS_SUCCESS:
            print("is_AOI ERROR")

        nRet = ueye.is_AllocImageMem(self.hCam, self.rectAOI.s32Width, self.rectAOI.s32Height,
                                     self.nBitsPerPixel, self.pcImageMemory, self.MemID)
        if nRet != ueye.IS_SUCCESS:
            print("is_AllocImageMem ERROR")
        else:
            # Makes the specified image memory the active memory
            nRet = ueye.is_SetImageMem(self.hCam, self.pcImageMemory, self.MemID)
            if nRet != ueye.IS_SUCCESS:
                print("is_SetImageMem ERROR")
            else:
                # Set the desired color mode
                nRet = ueye.is_SetColorMode(self.hCam, self.m_nColorMode)

    def capture_video(self):
        nRet = ueye.is_CaptureVideo(self.hCam, ueye.IS_DONT_WAIT)
        if nRet != ueye.IS_SUCCESS:
            print("is_CaptureVideo ERROR")

        # Enables the queue mode for existing image memory sequences
        nRet = ueye.is_InquireImageMem(self.hCam, self.pcImageMemory, self.MemID, self.rectAOI.s32Width,
                                       self.rectAOI.s32Height, self.nBitsPerPixel, self.pitch)
        if nRet != ueye.IS_SUCCESS:
            print("is_InquireImageMem ERROR")

        fps = ueye.DOUBLE()
        ueye.is_SetFrameRate(self.hCam, ueye.IS_GET_FRAMERATE, fps)
        print(fps)

    def get_image(self):
        # Extract data from our image memory...
        array = ueye.get_data(self.pcImageMemory, self.rectAOI.s32Width, self.rectAOI.s32Height,
                              self.nBitsPerPixel, self.pitch, copy=False)

        # ...and reshape it in an numpy array
        frame = np.reshape(array, (self.rectAOI.s32Height.value, self.rectAOI.s32Width.value, self.bytes_per_pixel))

        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        return frame

    def exit_camera(self):
        ueye.is_FreeImageMem(self.hCam, self.pcImageMemory, self.MemID)

        # Disables the hCam camera handle and releases the data structures and memory areas taken up by the uEye camera
        ueye.is_ExitCamera(self.hCam)