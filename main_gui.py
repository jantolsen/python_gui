# Graphical User Interface
# ------------------------------
# Description:
# Create a graphical user interface
# Allowing for screening statuses 
# and operator inputs

# Version
# ------------------------------
# 0.0   -   Initial version
#           [06.07.2022] - Jan T. Olsen

# Import packages
# ------------------------------
import sys
import time

# PyQt packages
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal, QRunnable, QObject, QThread, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets

# Import Class Files
from ui.main_window import Ui_MainWindow
from ctrl.ctrl_gamepad import Gamepad


# Gamepad Worker Class
# ------------------------------
# Defined as a separate QThread
class GamepadWorker(QThread):

    # Class signals
    progressbar_value = pyqtSignal(int)

    # Class constructor
    # ------------------------------
    def __init__(self):
        super(GamepadWorker, self).__init__()

        # Declare XBOX Gamepad class
        self.XBOX = Gamepad()

    # QThread run-function
    # ------------------------------
    @pyqtSlot()
    def run(self):

        # Infinite loop
        while True: 
            # Read XBOX Button values
            A, X, B, Y = self.XBOX.read_button()

            # Read XBOX Joystick values
            JoyLeft_X, JoyLeft_Y, JoyRight_X, JoyRight_Y = self.XBOX.read_joystick()

            # Emit Class signal
            self.progressbar_value.emit(JoyLeft_X) 
            time.sleep(0.01)

# Controller Class
# ------------------------------
class AppWindow(QMainWindow):

    # Class constructor
    # ------------------------------
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()  

        # Initialize Gamepad-Worker Class
        self.xbox_worker = GamepadWorker()
        # Connect Gamepad-Worker' signal to "updateProgressBar_B"-function
        self.xbox_worker.progressbar_value.connect(self.updateProgressBar_B)
        # Start worker QThread
        self.xbox_worker.start()

        # Progressbar Setup
        self.ui.progressBar_A.setRange(0, 100)
        self.ui.progressBar_B.setRange(-100, 100)
        self.ui.progressBar_B.setFormat('%v%')  # Format: %p - percentage, %v - value

        # Button Setup
        # (Connect button-press with designated functions)
        self.ui.pushButton_A.clicked.connect(self.buttonA_Pressed) 
        self.ui.pushButton_B.clicked.connect(self.buttonB_Pressed)

    # Callback function - Button A Clicked 
    def buttonA_Pressed(self):
        print('Button A - Pressed')
        value_decrease = -5
        self.updateProgressBar_A(value_decrease)

    # Callback function - Button B Clicked 
    def buttonB_Pressed(self):
        print('Button B - Pressed')
        value_increase = 5
        self.updateProgressBar_A(value_increase)

    # Callback function - Progressbar A 
    def updateProgressBar_A(self, value):
        increment = value
        prev_value = self.ui.progressBar_A.value()
        self.ui.progressBar_A.setValue(increment + prev_value)

    # Callback function - Progressbar B
    def updateProgressBar_B(self, value):
        self.ui.progressBar_B.setValue(value)

# Main
# ------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    app.exec_()
    # sys.exit(app.exec_())