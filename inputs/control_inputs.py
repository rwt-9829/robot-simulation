"""
Author: Miguel Tamayo
Date: 09/09/2023

Contains the control input variables that are used to control the robot.
Control inputs are defined in the robot's moving frame
"""

class ControlInputs:
    def __init__(self, vl: float, vr: float) -> None:
        """
        controls inputs consist of left and right wheels to drive the robot
        @param: vl -> left wheel linear velocity [m/s]
        @param: vr -> right wheel linear velocity [m/s]
        """

        self.vl = vl
        self.vr = vr