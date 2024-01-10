"""
Author: Miguel Tamayo

controls.py
Contains controllers for the robot
"""

class P():
    """
    Proportional controller

    Inputs:
    -------
        kp (float): proportional gain

    return:
    -------
        p_controller (P): proportional controller
    """
    def __init__(self,
                 kp: float=0.0) -> None:

        self.kp = kp

    def update(self, command: float, current: float) -> float:
        """
        Calculates the controller's output (u)

        inputs:
        -------
            command (float): commanded / desired state
            current (float): current state
        
        return:
        -------
            u (float): controller output
        """

        e = command - current # error
        u = self.kp * e # controller output

        return u