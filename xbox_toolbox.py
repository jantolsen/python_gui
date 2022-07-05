# Controller Toolbox
# ------------------------------
# Description:
# Toolbox for utility classes and methods
# to be used with an external controller

# Version
# ------------------------------
# 0.0   -   Initial version
#           [05.07.2022] - Jan T. Olsen

# Import packages
from dataclasses import dataclass
from inputs import devices

# Dataclass - XBOX One Controller Constants
# ------------------------------
@dataclass()
class XBOX_CONST():
    """
    Xbox One - Controller Constants:
    """
    # Defining Axis Event-Key Constants
    AXIS_EVENT = 'Absolute'   # Axis Event
    JOYL_X = 'ABS_X'          # Joystick Left - Axis X
    JOYL_Y = 'ABS_Y'          # Joystick Left - Axis Y
    JOYR_X = 'ABS_RX'         # Joystick Right - Axis X
    JOYR_Y = 'ABS_RY'         # Joystick Right - Axis Y
    TRIG_L = 'ABS_Z'          # Trigger Left - Axis
    TRIG_R = 'ABS_RZ'         # Trigger Right - Axis

    # Defining Button Event-Key Constants
    BTN_EVENT = 'Key'         # Button Event
    DPAD_X = 'ABS_HAT0X'      # D-Pad - Axis X
    DPAD_Y = 'ABS_HAT0Y'      # D-Pad - Axis Y
    BTN_S = 'BTN_SOUTH'       # Button - South
    BTN_E = 'BTN_EAST'        # Button - East
    BTN_W = 'BTN_WEST'        # Button - West
    BTN_N = 'BTN_NORTH'       # Button - North
    BTN_LB = 'BTN_TL'         # Button - Left-Back Bumper No. 1
    BTN_RB = 'BTN_TR'         # Button - Right-Back Bumper No. 1  
    BTN_PBL = 'BTN_THUMBL'    # Button - Joystick Left Push
    BTN_PBR = 'BTN_THUMBR'    # Button - Joystick Right Push
    BTN_START = 'BTN_START'   # Button - Start
    BTN_SELECT = 'BTN_SELECT' # Button - Select

    # Defining Joystick Scaling Constants
    JOY_RAW_MIN = -32768  # Joystick Minimum Raw value
    JOY_RAW_MAX = 32767   # Joystick Maximum Raw value
    JOY_RAW_DB = 1000     # Joystick Deadband Raw value
    JOY_MIN = -100.0      # Joystick Minimum Scaling value
    JOY_MAX = 100.0       # Joystick Maximum Scaling value

    # Defining Trigger Scaling Constants
    TRIG_RAW_MIN = 0     # Joystick Minimum Raw value
    TRIG_RAW_MAX = 255   # Joystick Maximum Raw value
    TRIG_RAW_DB = 0      # Joystick Deadband Raw value
    TRIG_MIN = 0.0       # Joystick Minimum Scaling value
    TRIG_MAX = 100.0     # Joystick Maximum Scaling value

# Dataclass - Axis 
# ------------------------------
# Member related to Controller Axis
@dataclass()
class AxisData:
    
    # Declare Axis members
    JL_X    : int = 0    # Joystick Left - Axis X
    JL_Y    : int = 0    # Joystick Left - Axis Y
    JR_X    : int = 0    # Joystick Right - Axis X
    JR_Y    : int = 0    # Joystick Right - Axis Y
    LT      : int = 0    # Trigger Left - Axis
    RT      : int = 0    # Trigger Left - Axis
    
# Dataclass - Buttons 
# ------------------------------
# Members related to Controller Buttons
@dataclass()
class ButtonData:
    
    # Declare Button members
    A : bool = False        # Button - South
    B : bool = False        # Button - East
    X : bool = False        # Button - West
    Y : bool = False        # Button - North
    
    Start   : bool = False  # Button - Start
    Select  : bool = False  # Button - Select

    JL_PB : bool = False     # Joystick Left - Pushbutton
    JR_PB : bool = False     # Joystick Right - Pushbutton

    DPad_L : bool = False   # D-Pad - Left
    DPad_R : bool = False   # D-Pad - Right
    DPad_U : bool = False   # D-Pad - Up
    DPad_D : bool = False   # D-Pad - Down

    LB: bool = False       # Button - Left-Back Bumper
    RB: bool = False       # Button - Right-Back Bumper

# Get Connected Controller
# -----------------------------
def get_controller():
    """
    Get the first valid gamepad controller object
    (If no valid gamepad is connected an exception error is thrown)
    :return gampad: Gamepad object
    """

    # Using the first valid gamepad
    try:
        gamepad = devices.gamepads[0]

        # Return gamepad object
        return gamepad

    # Exception
    except IndexError: 
        # Print Error
        print('ERROR: getController: No connected gamepad found!')
        return None

# Scale Input Value
# -----------------------------
def calc_minmax_scaling(raw_value : int,
                        raw_min : int,
                        raw_max : int,
                        min : float,
                        max : float) -> float:
    """
    Rescale the raw input value from range [raw_min, raw_max] to a desired range [min, max]
    :param raw_value: Raw Input Value
    :param raw_min: Raw Minimum Value
    :param raw_max: Raw Maximum Value
    :param min: Scaled Minimum value
    :param max: Scaled Maximum value
    :return value: Scaled Value
    """

    # Scaling input-value to range: [0 , 1]
    tmp_value = (raw_value - raw_min) / (raw_max - raw_min)

    # Scaling input-value to range: [min , max]
    value = tmp_value * (max - min) + min

    return value

# Scale Input Value with Deadband
# -----------------------------
def calc_minmax_scaling_deadband(raw_value : int,
                                 raw_min : int,
                                 raw_max : int,
                                 raw_db : int,
                                 min : float,
                                 max : float) -> float:
    """
    Rescale the raw input value from range [raw_min, raw_max] to a desired range [min, max]
    with neglecting Deadband value on the raw input value 
    :param raw_value: Raw Input Value
    :param raw_min: Raw Minimum Value
    :param raw_max: Raw Maximum Value
    :param raw_db:  Raw Deadband Value
    :param min: Scaled Minimum value
    :param max: Scaled Maximum value
    :return value: Scaled Value
    """

    # Use local variable
    tmp_raw_value = 0
    tmp_raw_min = raw_min + raw_db
    tmp_raw_max = raw_max - raw_db
    tmp_raw_db_neg = (-1) * raw_db 
    tmp_raw_db_pos = raw_db

    # Deadband Calculation
    # -----------------------------
    # Raw value is whithin deadband range
    if (abs(raw_value) < abs(raw_db)):
        tmp_raw_value = 0

    # Raw value is below deadband range
    elif (raw_value < tmp_raw_db_neg):
        tmp_raw_value = raw_value + raw_db

    # Raw value is above deadband range
    elif (raw_value > tmp_raw_db_pos):
        tmp_raw_value = raw_value - raw_db

    # Rescaling
    # -----------------------------
    # Scaling input-value to range: [0 , 1]
    tmp_value = (tmp_raw_value - tmp_raw_min) / (tmp_raw_max - tmp_raw_min)

    # Scaling input-value to range: [min , max]
    value = tmp_value * (max - min) + min

    return value

# Scale Joystick Input Value with Deadband
# -----------------------------
def scale_input_joystick(raw_value : int) -> float:
    """
    Rescale the raw Joystick input value from range [raw_min, raw_max] to a desired range [min, max]
    with neglecting Joystick Deadband.
    Using Joystick Scaling Constans Dataclass (XBOX_CONST)
    :param raw_value: Raw Input Value
    :param JOY_SCALE: Joystick Scaling Constans Dataclass 
    :return value: Scaled Value
    """
    
    joy_value = calc_minmax_scaling_deadband(raw_value, 
                                             XBOX_CONST.JOY_RAW_MIN,
                                             XBOX_CONST.JOY_RAW_MAX,
                                             XBOX_CONST.JOY_RAW_DB,
                                             XBOX_CONST.JOY_MIN,
                                             XBOX_CONST.JOY_MAX)
    
    return joy_value

# Scale Trigger Input Value with Deadband
# -----------------------------
def scale_input_trigger(raw_value : int) -> float:
    """
    Rescale the raw Trigger input value from range [raw_min, raw_max] to a desired range [min, max]
    with neglecting Trigger Deadband 
    Using Trigger Scaling Constans Dataclass (XBOX_CONST)
    :param raw_value: Raw Input Value
    :return value: Scaled Value
    """
    
    trigger_value = calc_minmax_scaling_deadband(raw_value, 
                                                 XBOX_CONST.TRIG_RAW_MIN,
                                                 XBOX_CONST.TRIG_RAW_MAX,
                                                 XBOX_CONST.TRIG_RAW_DB,
                                                 XBOX_CONST.TRIG_MIN,
                                                 XBOX_CONST.TRIG_MAX)
    
    return trigger_value