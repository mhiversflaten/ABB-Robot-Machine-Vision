import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
import numpy as np
import Puck
import math


def QR_Scanner(img):
    """Scan QR codes from image. Returns position, orientation and image with marked QR codes"""

    # TODO: Make an adaptive bilateralFilter that depends on camera_height
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Make grayscale image for filtering and thresholding
    blur = cv2.bilateralFilter(src=grayscale, d=3, sigmaColor=75, sigmaSpace=75)
    normalized_img = cv2.normalize(blur, blur, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=-1)
    data = decode(normalized_img, symbols=[ZBarSymbol.QRCODE])
    puck_list = []
    width_list = []

    sorted_data = sorted(data, key=lambda x: x[0])  # Sort the QR codes in ascending order

    for QR_Code in sorted_data:  # Go through all QR codes

        points = QR_Code.polygon  # Extract two corner points
        x1 = points[0][0]
        y1 = points[0][1]
        x2 = points[3][0]
        y2 = points[3][1]

        angle = np.rad2deg(np.arctan2(-(y2 - y1), x2 - x1))  # Calculate the orientation of each QR code

        x = [p[0] for p in points]
        y = [p[1] for p in points]
        position = [sum(x) / len(points), sum(y) / len(points)]  # Calculate center of each QR code

        width, height, channels = img.shape
        position = [position[0] - height/2, position[1] - width/2]  # Make center of image (0,0)

        puck = str(QR_Code.data, "utf-8")  # Convert QR code data to string
        puck_number = int(''.join(filter(str.isdigit, puck)))  # Find only puck number from QR code string

        # Calculate distance between (x1,y1) and (x2,y2) to understand height of pucks:
        qr_width = math.hypot((x2 - x1), (y2 - y1))
        print("width", qr_width)
        #width_list.append((puck_number, qr_width))

        # Make the puck object and add it to the puck list
        puck = Puck.Puck(puck_number, position, angle, qr_width)
        puck_list.append(puck)

    return puck_list


def QR_Scanner_visualized(img):
    """Scan QR codes from image. Returns position, orientation and image with marked QR codes"""

    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Make grayscale image for filtering and thresholding
    blur = cv2.bilateralFilter(src=grayscale, d=3, sigmaColor=75, sigmaSpace=75)
    normalized_img = cv2.normalize(blur, blur, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=-1)
    data = decode(normalized_img, symbols=[ZBarSymbol.QRCODE])

    normalized_img = cv2.cvtColor(normalized_img, cv2.COLOR_GRAY2BGR)

    # Thresholding for greater contrast:
    #ret, threshBlur = cv2.threshold(grayscale, 50 + thresh_incr, 255, cv2.THRESH_BINARY)
    sorted_data = sorted(data, key=lambda x: x[0])  # Sort the QR codes in ascending order

    for QR_Code in sorted_data:  # Go through all QR codes
        polygon = np.int32([QR_Code.polygon])  # Convert from int64 to int32, polylines only accepts int32
        cv2.polylines(normalized_img, polygon, True, color=(0, 0, 255), thickness=10)  # Draw lines around QR-codes

        points = polygon[0]  # Extract corner points

        x = [p[0] for p in points]
        y = [p[1] for p in points]
        position = (sum(x) / len(points), sum(y) / len(points))  # Calculate center of each QR code

        # width, height, channels = img.shape
        # cv2.circle(normalized_img, center=(int(height/2), int(width/2)), radius=10, color=(0,0,0), thickness=-1)

        # Draw circles in the middle of QR codes:
        # cv2.circle(normalized_img, center=(int(position[0]), int(position[1])), radius=10, color=(255, 0, 0), thickness=-1)

    return normalized_img
