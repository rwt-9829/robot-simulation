"""
Author: Miguel Tamayo

control_inputs.py
Contains the control input variables that are used to control the robot.
Control inputs are defined in the robot's moving frame
"""

class ControlInputs:
    """
    controls inputs consist of left and right wheels to drive the robot

    inputs:
    -------
        vl (float): left wheel linear velocity [m/s]
        vr (float): right wheel linear velocity [m/s]

    return:
    -------
        inputs (ControlInputs): robot's inputs
    """
    def __init__(self,
                 vl: float,
                 vr: float) -> None:
        
        self.vl = vl
        self.vr = vr