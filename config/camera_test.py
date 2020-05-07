import config_independent
import cv2

cam = config_independent.Camera()
cam.init()
cam.set_parameters()
cam.allocate_memory()
cam.capture_video()

while True:
    img = cam.get_image()
    cv2.imshow("test", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

cam.exit_camera()