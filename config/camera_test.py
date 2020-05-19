from image_tools import Camera, ImageFunctions
# importing required libraries of opencv
import cv2

# importing library for plotting
from matplotlib import pyplot as plt

cam = Camera.Camera()
cam.init()
cam.set_parameters()
cam.allocate_memory()
cam.capture_video()

#img = ImageFunctions.capture_image(cam, 60)
#img = ImageFunctions.QR_Scanner_visualized(img)
img = cv2.imread("image.png")
img = ImageFunctions.QR_Scanner_visualized(img)
cv2.imwrite("bilateral.jpg", img)
histr = cv2.calcHist([img], [0], None, [256], [0, 256])

# show the plotting graph of an image
plt.plot(histr)
plt.show()
#cv2.imshow("test", img)
cv2.waitKey(0)

cam.exit_camera()