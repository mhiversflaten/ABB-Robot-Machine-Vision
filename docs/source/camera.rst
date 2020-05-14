Camera class
============

The Camera class contains methods specifically meant for the University of Stavanger.
These functions have only been tested on a IDS UI-1007XS-C camera, and might not work
correctly as intended on other models.

The Camera class makes it possible to initalize a uEye camera, set parameters, and start video capture.

Quickstart
^^^^^^^^^^

.. code-block:: python

    # Initialization
    cam = Camera()
    cam.init()
    cam.set_parameters()
    cam.allocate_memory()
    cam.capture_video()

    # Show video
    img = cam.get_image()
    cv2.imshow("Quickstart", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    cam.exit_camera()