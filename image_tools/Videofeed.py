# Importing necessary libraries, mainly the OpenCV, and PyQt libraries
import cv2
import numpy as np
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QPoint


class ShowVideo(QtCore.QObject):
    # initiating the built in camera
    camera_port = 1
    camera = cv2.VideoCapture(camera_port)
    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):
        run_video = True
        while run_video:
            ret, image = self.camera.read()

            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            height, width, _ = color_swapped_image.shape

            qt_image = QtGui.QImage(color_swapped_image.data,
                                    width,
                                    height,
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)

            self.VideoSignal.emit(qt_image)


class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('Test')

        thread = QtCore.QThread()
        thread.start()
        vid = ShowVideo()
        vid.moveToThread(thread)
        image_viewer = ImageViewer()

        vid.VideoSignal.connect(image_viewer.setImage)

        # Button to start the videocapture:

        push_button = QtWidgets.QPushButton('Start')
        push_button.clicked.connect(vid.startVideo)
        vertical_layout = QtWidgets.QVBoxLayout()

        b1 = QtWidgets.QPushButton('TESTING')
        b1.move(0, 0)
        b1.clicked.connect(image_viewer.print)

        vertical_layout.addWidget(b1)
        vertical_layout.addWidget(image_viewer)
        vertical_layout.addWidget(push_button)

        layout_widget = QtWidgets.QWidget()
        layout_widget.setLayout(vertical_layout)


    def print(self):
        print("it worked")


    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = ImageViewer()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())