"""
Author: Miguel Tamayo

control_inputs.py
Contains different classes that are used to control the robot
"""

class WheelLinearInputs:
    """
    Left and right wheel linear velocities in the local frame

    inputs:
    -------
        vl (float): left wheel linear velocity [m/s]
        vr (float): right wheel linear velocity [m/s]

    return:
    -------
        inputs (WheelLinearInputs): robot's inputs
    """
    def __init__(self,
                 vl: float,
                 vr: float) -> None:
        
        self.vl = vl
        self.vr = vr