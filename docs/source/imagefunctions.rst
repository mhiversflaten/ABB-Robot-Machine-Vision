Image Tools
===========

The image tools included in the ABB-Robot-Machine-Vision package are mainly
directed toward `uEye cameras`_.
These tools utilize IDS's Python bindings for the uEye API: PyuEye_.

.. _PyuEye: https://pypi.org/project/pyueye/
.. _uEye cameras: https://en.ids-imaging.com/

Camera Class
^^^^^^^^^^^^

.. py:class:: Camera(cam_ID=0)

    The Camera class contains methods specifically meant for the University of Stavanger.
    These functions have only been tested on a IDS UI-1007XS-C camera, and might not work
    as intended on other models.

Quickstart
**********

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

The parameters set are not currently configurable through method inputs.
They are specifically set for laboratory work at the University of Stavanger.


Capturing Images and Video
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:function:: capture_image(cam, gripper_height)

    Manually adjusts the camera focus through :py:func:`calculate_focus`.
    Captures a single image through PyuEye functions.
    Focus is manually adjusted depending on the working distance.

    :param Camera cam: A :py:class:`Camera` object
    :param int gripper_height: The height of the gripper above the work object

    :return: An image

.. py:function:: showVideo(cam)

    Continuously displays the robot's view in an OpenCV imshow window.
    The video uses :py:func:`QR_Scanner_visualized` to visualize the scanned QR codes.
    :py:func:`showVideo` works well in threads:

    .. code-block:: python

        # Show video feed in separate thread
        cam_thread = threading.Thread(target=ImageFunctions.showVideo,
                     args=(cam,), daemon=True)
        cam_thread.start()

    Single images can still be retrieved through
    :py:func:`capture_image` while the thread is active.

    :param Camera cam: A :py:class:`Camera` object

.. py:function:: calculate_focus(cam, working_distance)

    Calculates the correct focus value for a specific IDS XS
    camera with some working distance.
    The focus value is found by comparing the working distance to a characteristic.
    This characteristic is *unique* to the XS camera with serial code 4102885308.
    This function should be accurate for working distances up to 620mm.

    :param Camera cam: A :py:class:`Camera` object
    :param int working_distance: Distance from camera lens to subject in millimeters

.. py:function:: findPucks(cam, robot, robtarget_pucks, cam_comp=False, number_of_images=1)

    Finds all pucks in the images taken and puts them in a list.
    The positions of all pucks are then converted to robtargets using
    :py:func:`create_robtarget`.

    If pucks that were previously found are found once again, they will not be re-added
    to the puck list, so that only new pucks are transformed into robtargets.

    :param Camera cam: A :py:class:`Camera` object
    :param RWS robot: An :py:class:`RWS` object
    :param Puck[] robtarget_pucks: All pucks found previously
    :param bool cam_comp: True if camera adjustment should be run,
        False if it has already been run
    :param int number_of_images: How many images should be taken in
        the attempt to find all pucks

    :return: A list with all found pucks, without duplicates


Scanning QR Codes
^^^^^^^^^^^^^^^^^

.. py:function:: QR_Scanner(img)

    Filters and normalizes the input image. The processed image is decoded using pyzbar_.
    For every QR code detected, a :py:class:`Puck` object is created.

    :param ndarray img: An image

    :return: A list of :py:class:`Puck` objects

The QR scanner function uses software from ZBar_ through pyzbar_. The image passed to the
function is first filtered and transformed into a normalized grayscale image. The grayscale
image is decoded by ZBar to extract information from QR codes in the image.

.. py:function:: QR_Scanner_visualized(img)

    Filters and normalizes the input image. The processed image is decoded using pyzbar_.
    QR codes found in the image are marked with red squares for display.

    :param ndarray img: An image

    :return: Image for display

.. _ZBar: http://zbar.sourceforge.net/
.. _pyzbar: https://pypi.org/project/pyzbar/
