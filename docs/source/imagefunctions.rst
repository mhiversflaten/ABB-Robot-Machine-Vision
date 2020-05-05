Image Tools
===========

The image tools included in the ABB-Klosser package are mainly directed toward `uEye cameras`_.
These tools utilize IDS's Python bindings for the uEye API: PyuEye_.

.. _PyuEye: https://pypi.org/project/pyueye/
.. _uEye cameras: https://en.ids-imaging.com/

=======
The image tools included in the ABB-Klosser package are mainly directed toward :ref:`uEye cameras`_ [[fix this link]].
These tools utilize IDS's Python bindings for the uEye API: pyuEye_.

.. _pyuEye: https://pypi.org/project/pyueye/
.. _uEye cameras: https://en.ids-imaging.com/

Capturing Images and Video
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:function:: capture_image(cam, gripper_height)

    Triggers autofocus once and captures an image using pyuEye functions.

    :param Camera cam: A Camera object

Some random text

Scanning QR Codes
^^^^^^^^^^^^^^^^^

The QR scanner function uses software from ZBar_ through pyzbar_. The image passed to the
function is first filtered and transformed into a normalized grayscale image. The grayscale
image is decoded by ZBar to extract information from QR codes in the image.

.. _ZBar: http://zbar.sourceforge.net/
.. _ZBar: https://pypi.org/project/pyzbar/

.. py:function:: QR_Scanner(img)

    Filters and normalizes the input image. The resulting image is decoded using pyzbar_.
    For every QR code detected, a :ref:`Puck object` is created.

    :param ndarray img: An image

    :return: A list of Puck objects

.. _pyzbar: https://pypi.org/project/pyzbar/

