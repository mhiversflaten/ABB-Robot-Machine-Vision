Image Tools
===========

The image tools included in the ABB-Klosser package are mainly directed toward `uEye cameras`_.
These tools utilize IDS's Python bindings for the uEye API: PyuEye_.

.. _PyuEye: https://pypi.org/project/pyueye/
.. _uEye cameras: https://en.ids-imaging.com/

Scanning QR Codes
^^^^^^^^^^^^^^^^^

The QR scanner function uses software from ZBar_ through pyzbar_. The image passed to the
function is first filtered and transformed into a normalized grayscale image. The grayscale
image is decoded by ZBar to extract information from QR codes in the image.

.. py:function:: QR_Scanner(img)

    Filters and normalizes the input image. The processed image is decoded using pyzbar_.
    For every QR code detected, a :ref:`Puck object` is created.

    :param ndarray img: An image

    :return: A list of Puck objects

.. py:function:: QR_Scanner_visualized(img)

    Filters and normalizes the input image. The processed image is decoded using pyzbar_.
    QR codes found in the image are marked with red squares for display.

    :param ndarray img: An image

    :return: Image for display

.. _ZBar: http://zbar.sourceforge.net/
.. _pyzbar: https://pypi.org/project/pyzbar/


Capturing Images and Video
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:function:: capture_image(cam, gripper_height)

    Captures a single image through PyuEye functions.
    Focus is manually adjusted depending on the working distance.

    :param Camera cam: A :ref:`Camera object`
    :param int gripper_height: The height of the gripper above the work object

    :return: An image

.. py:function:: showVideo(cam)

    Continuously displays the robot's view in an OpenCV imshow window.
    The video uses :py:func:`QR_Scanner_visualized` to visualize the scanned QR codes.
    :py:func:`showVideo` works well in threads::

        test some code

    :param Camera cam: A :ref:`Camera object`