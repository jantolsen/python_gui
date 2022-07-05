# Controller
# ------------------------------
# Description:
# Read input values from external gamepad Controller

# Version
# ------------------------------
# 0.0   -   Initial version
#           [20.06.2022] - Jan T. Olsen

# Import packages
import threading
import time

# Import Toolbox
import xbox_toolbox as Toolbox

# Controller Class
# ------------------------------
class Controller():

    # Class constructor
    # ------------------------------
    def __init__(self):

        # Search for connected controller
        # (using CtrlToolbox. function)
        self.gamepad = Toolbox.get_controller()

        # Define Controller Members
        # (based on Dataclasses from Controller-Toolbox)
        self.AxisData = Toolbox.AxisData()
        self.ButtonData = Toolbox.ButtonData()

        # # Configure thread
        self._monitor_thread = threading.Thread(target=self.XBOX_ControllerMonitor, args=())
        self._monitor_thread.daemon = True

        # Start XBOX-Controller-Monitor
        self._monitor_thread.start()

    def read_button(self):

        A = self.ButtonData.A
        X = self.ButtonData.X
        B = self.ButtonData.B
        Y = self.ButtonData.Y

        return (A, B, X, Y)

    def read_joystick(self):

        JoyLeft_X = Toolbox.scale_input_joystick(self.AxisData.JL_X)
        JoyLeft_Y = Toolbox.scale_input_joystick(self.AxisData.JL_Y)
        JoyRight_X = Toolbox.scale_input_joystick(self.AxisData.JR_X)
        JoyRight_Y = Toolbox.scale_input_joystick(self.AxisData.JR_Y)

        return (JoyLeft_X, JoyLeft_Y, JoyRight_X, JoyRight_Y)


    # XBOX Controller Monitor
    # ------------------------------    
    def XBOX_ControllerMonitor(self):
        
        # While-Loop for detecting controller inputs
        while(True):
            
            # Get Controller Action from reading Gamepad object
            events = self.gamepad.read()

            # Loop through all event in events
            for event in events:

                # Axis Event
                # Incomming Axis-Input from Controller (integer values)
                if event.ev_type == Toolbox.XBOX_CONST.AXIS_EVENT:
                    
                    # Joystick Left - Axis X
                    if event.code == Toolbox.XBOX_CONST.JOYL_X:
                        self.AxisData.JL_X = event.state

                    # Joystick Left - Axis Y
                    elif event.code == Toolbox.XBOX_CONST.JOYL_Y:
                        self.AxisData.JL_Y = event.state

                    # Joystick Right - Axis X
                    elif event.code == Toolbox.XBOX_CONST.JOYR_X:
                        self.AxisData.JR_X = event.state

                    # Joystick Right - Axis Y
                    elif event.code == Toolbox.XBOX_CONST.JOYR_Y:
                        self.AxisData.JR_Y = event.state

                    # Trigger Left - Axis
                    elif event.code == Toolbox.XBOX_CONST.TRIG_L:
                        self.AxisData.LT = event.state

                    # Trigger Right - Axis
                    elif event.code == Toolbox.XBOX_CONST.TRIG_R:
                        self.AxisData.RT = event.state

                    # D-PAD - Left / Right
                    elif event.code == Toolbox.XBOX_CONST.DPAD_X:
                        
                        # Determine Left/Right by sign of state-value
                        if event.state < 0:
                            self.ButtonData.DPad_L = event.state
                        elif event.state > 0:
                            self.ButtonData.DPad_R = event.state
                        # Reset D-PAD - Left / Right values
                        else:
                            self.ButtonData.DPad_L = event.state
                            self.ButtonData.DPad_R = event.state
                        
                    # D-PAD - Up / Down
                    elif event.code == Toolbox.XBOX_CONST.DPAD_Y:

                        # Determine Up/Down by sign of state-value
                        if event.state < 0:
                            self.ButtonData.DPad_U = event.state
                        elif event.state > 0:
                            self.ButtonData.DPad_D = event.state
                        # Reset D-PAD - Up / Down values
                        else:
                            self.ButtonData.DPad_U = event.state
                            self.ButtonData.DPad_D = event.state

                # Button Event
                # Incomming Button-Input from Controller (bool values)
                if event.ev_type == Toolbox.XBOX_CONST.BTN_EVENT:
                    
                    # Button - A
                    if event.code == Toolbox.XBOX_CONST.BTN_S:
                        self.ButtonData.A = event.state

                    # Button - B
                    elif event.code == Toolbox.XBOX_CONST.BTN_E:
                        self.ButtonData.B = event.state

                    # Button - X
                    elif event.code == Toolbox.XBOX_CONST.BTN_W:
                        self.ButtonData.X = event.state

                    # Button - Y
                    elif event.code == Toolbox.XBOX_CONST.BTN_N:
                        self.ButtonData.Y = event.state

                    # Button - Left-Back Bumper No. 1
                    elif event.code == Toolbox.XBOX_CONST.BTN_LB:
                        self.ButtonData.LB = event.state

                    # Button - Right-Back Bumper No. 1
                    elif event.code == Toolbox.XBOX_CONST.BTN_RB:
                        self.ButtonData.RB = event.state

                    # Button - Joystick Left Push
                    elif event.code == Toolbox.XBOX_CONST.BTN_PBL:
                        self.ButtonData.JL_PB = event.state

                    # Button - Joystick Right Push
                    elif event.code == Toolbox.XBOX_CONST.BTN_PBR:
                        self.ButtonData.JR_PB = event.state

                    # Button - Start
                    elif event.code == Toolbox.XBOX_CONST.BTN_START:
                        self.ButtonData.Start = event.state

                    # Button - Select
                    elif event.code == Toolbox.XBOX_CONST.BTN_SELECT:
                        self.ButtonData.Select = event.state