Image Tools
===========

.. _pyuEye: https://pypi.org/project/pyueye/
.. _uEye cameras: https://en.ids-imaging.com/

The image tools included in the ABB-Klosser package are mainly directed toward :ref:`uEye cameras`.
These tools utilize IDS's Python bindings for the uEye API: pyuEye_.



Capturing Images and Video
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:function:: capture_image(cam, gripper_height)

    Triggers autofocus once and captures an image using pyuEye functions.

    :param Camera cam: A Camera object

Some random text

Scanning QR Codes
^^^^^^^^^^^^^^^^^

.. py:function:: QR_Scanner(img)

    Filters and normalizes the input image. The resulting image is decoded using pyzbar_. For every QR code detected,
    a :ref:`Puck object` is created.

    :param ndarray img: An image

    :return: A list of Puck objects

.. _pyzbar: https://pypi.org/project/pyzbar/

