import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from Ui_color import Ui_MainWindow
import cv2
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#upper: [83,255,255]  lower: [38,47,152]
class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.pushButton.clicked.connect(self.opencam)
        self.pushButton_2.clicked.connect(self.hui)
        self.camera = QTimer(self)
        self.HSV_num = QTimer(self)
        self.HSV_num.timeout.connect(self.num)
        self.num()
        self.horizontalSlider.valueChanged.connect(self.num)
        self.horizontalSlider_2.valueChanged.connect(self.num)
        self.horizontalSlider_3.valueChanged.connect(self.num)
        self.horizontalSlider_4.valueChanged.connect(self.num)
        self.horizontalSlider_5.valueChanged.connect(self.num)
        self.horizontalSlider_6.valueChanged.connect(self.num)
    def hui(self):
        self.horizontalSlider.setValue(0)
        self.horizontalSlider_2.setValue(0)
        self.horizontalSlider_3.setValue(0)
        self.horizontalSlider_4.setValue(255)
        self.horizontalSlider_5.setValue(255)
        self.horizontalSlider_6.setValue(255)
    def opencam(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,320) #设置分辨率
        self.cap.set(4,240)
        self.camera.timeout.connect(self.cam)
        self.camera.start(10)
    def num(self):
            self.label_10.setText(str(self.horizontalSlider.value()))
            self.label_11.setText(str(self.horizontalSlider_2.value()))
            self.label_13.setText(str(self.horizontalSlider_3.value()))
            self.label_14.setText(str(self.horizontalSlider_4.value()))
            self.label_15.setText(str(self.horizontalSlider_5.value()))
            self.label_12.setText(str(self.horizontalSlider_6.value()))
            self.h_min=self.horizontalSlider.value()
            self.s_min=self.horizontalSlider_2.value() 
            self.v_min=self.horizontalSlider_3.value() 
            self.h_max=self.horizontalSlider_4.value() 
            self.s_max=self.horizontalSlider_5.value() 
            self.v_max=self.horizontalSlider_6.value() 
            self.textEdit.setText("upper: ["+str(self.h_max)+","+str(self.s_max)+","+str(self.v_max)+"]"+"  lower: ["+str(self.h_min)+","+str(self.s_min)+","+str(self.v_min)+"]")
    def cam(self):
        success, frame=self.cap.read()
        if success:
            imgHsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            lower = np.array([self.h_min,self.s_min,self.v_min])
            upper = np.array([self.h_max,self.s_max,self.v_max])
            mask = cv2.inRange(imgHsv,lower,upper)
            result = cv2.bitwise_and(frame,frame, mask = mask)
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            hStack = np.hstack([frame,mask,result])
            show2 = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            show3 = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            ret, binary = cv2.threshold(show3,127,255,cv2.THRESH_BINARY)
            contours,hierarchy = cv2.findContours(binary,mode=cv2.RETR_TREE,method=cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                c = max(contours, key=cv2.contourArea)
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            showimage2 = QImage(show2.data, show2.shape[1], show2.shape[0], QImage.Format_RGB888)
            self.label_2.setPixmap(QPixmap.fromImage(showimage2))
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showimage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(showimage))

    
if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(App.exec_())