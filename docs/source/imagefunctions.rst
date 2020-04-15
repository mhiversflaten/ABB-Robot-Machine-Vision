Image Tools
===========

The image tools included in the ABB-Klosser package are mainly directed toward uEye_ `cameras`__.
These tools utilize IDS's Python bindings for the uEye API: pyuEye_.

.. _pyuEye: https://pypi.org/project/pyueye/
.. _uEye: https://en.ids-imaging.com/

Capturing Images and Video
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:function:: capture_image(cam, gripper_height)

    Triggers autofocus once and captures an image using pyuEye functions.

    :param Camera cam: A Camera object

Some random text

Scanning QR Codes
^^^^^^^^^^^^^^^^^

.. py:function:: QR_Scanner(img)

    Filters and normalizes the input image. The resulting image is decoded using :ref:`Puck`. For every QR code detected,
    a Puck_ object is created.

.. _pyzbar: https://pypi.org/project/pyzbar/

