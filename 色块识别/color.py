import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from Ui_color import Ui_MainWindow
import cv2
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
    
class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.opencam)
        self.camera = QTimer(self)

    def opencam(self):
        self.cap = cv2.VideoCapture(0)
        self.camera.timeout.connect(self.cam)
        self.camera.start(10)
    
    def cam(self):
        success, frame=self.cap.read()
        if success:
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showimage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(showimage))

    
if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(App.exec_())