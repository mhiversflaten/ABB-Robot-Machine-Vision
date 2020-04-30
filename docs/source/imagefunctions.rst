Image Tools
===========

The image tools included in the ABB-Klosser package are mainly directed toward `uEye cameras`_.
These tools utilize IDS's Python bindings for the uEye API: PyuEye_.

.. _PyuEye: https://pypi.org/project/pyueye/
.. _uEye cameras: https://en.ids-imaging.com/

QR Scanner
^^^^^^^^^^

The QR scanner function uses software from ZBar_ through pyzbar_. The image passed to the
function is first filtered and transformed into a normalized grayscale image. The grayscale
image is decoded by ZBar to extract information from QR codes in the image.

.. _ZBar: http://zbar.sourceforge.net/
.. _ZBar: https://pypi.org/project/pyzbar/

.. py:function:: QR_Scanner(img)

    :param numpy.ndarray img:


.. py:function:: capture_image(cam, gripper_height)

    Triggers autofocus once and captures an image using pyuEye functions.

    :param Camera cam: A Camera object

Some random text
