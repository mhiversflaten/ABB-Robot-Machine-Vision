from image_tools import Camera
import cv2

cam = Camera.Camera()
cam.init()
cam.set_parameters()
cam.allocate_memory()
cam.capture_video()

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi', -1, 15.0, (640, 480))

while True:
    img = cam.get_image()
    out.write(img)
    cv2.imshow("test", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

out.release()
cam.exit_camera()