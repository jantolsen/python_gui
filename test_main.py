import sys
import threading
import time

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import pyqtSignal, QRunnable, QObject, QThread, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.test_main_window import Ui_Dialog

from xbox_controller import Controller

class WorkerSignals(QObject):
    
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


# class Worker(QRunnable):
# class Worker(QObject):
class Worker(QThread):
    barvalue = pyqtSignal(int)
    def __init__(self):
        super(Worker, self).__init__()

        self.XBOX = Controller()

        # self.run
        # thread = QThread()
        # thread.start()

        # self.XBOX.XBOX_ControllerMonitor.moveToThread(thread)

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        while 1: 
            A, X, B, Y = self.XBOX.read_button()
            
            JoyLeft_X, JoyLeft_Y, JoyRight_X, JoyRight_Y = self.XBOX.read_joystick()

            if A:
                val = 50

            elif B:
                val = 75
            else:
                val = 25

            self.barvalue.emit(val) 
            time.sleep(0.5)


class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()  

        # self.XBOX = Controller()

        # thread = QThread()
        # thread.start()

        # xbox = Worker()
        # xbox.moveToThread(thread)

        self.xbox = Worker()
        self.xbox.barvalue.connect(self.updateProgressBar2)
        #connect(self.updateProgressBar)
        self.xbox.start()

        self.ui.progressBar.setRange(0, 100)
        self.ui.pushButton_A.clicked.connect(self.buttonA_Pressed)
        self.ui.pushButton_B.clicked.connect(self.buttonB_Pressed)


    # def updateController(self):
    #     (A,B,X,Y) = self.XBOX.read_button()

    #     print(A,B,X,Y)

    def buttonA_Pressed(self):
        print('Button A - Pressed')
        self.updateProgressBar(90)

    def buttonB_Pressed(self):
        print('Button B - Pressed')
        self.updateProgressBar(10)

    def updateProgressBar(self, value):
        self.ui.progressBar.setValue(value)

    def updateProgressBar2(self, value):
        self.ui.progressBar.setValue(value)

# Main
# ------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    # w.updateController()
    w.show()
    
    app.exec_()
    # sys.exit(app.exec_())