"""
Author: Miguel Tamayo

states.py
Contains classes describing the robot states
"""

import numpy as np

class RobotState:
    """
    Defines vehicle's current position

    inputs:
    -------
        px (float): initial robot x position in global frame [m]
        py (float): initial robot y position in global frame [m]
        phi (float): initial robot orientation [rad]

    return:
    -------
        state (RobotState): robot's state instance
    """
    def __init__(self,
                 px: float = 0.0,
                 py: float = 0.0,
                 phi: float = 0.0) -> None:
        # state vector
        self.px = px
        self.py = py
        self.phi = phi

    def __str__(self) -> str:
        """
        formats robot state into string
        """
        return f"x: {self.px}, y: {self.py}, heading: {self.phi}"

        
class RobotDerivativeState:
    """
    defines robot's rates

    inputs:
    -------
        local_v (float): linear velocity in the robot's local frame
        vx (float): robot x velocity in global frame [m/s]
        vy (float): robot y velocity in global frame [m/s]
        r_rate (float): robot turning rate [rad/s]

    return:
    -------
        derivative (RobotDerivativeState): robot's derivative instance
    """
    def __init__(self,
                 vx: float = 0.0,
                 vy: float = 0.0,
                 r_rate: float = 0.0) -> None:
        # derivative state vector
        self.vx = vx
        self.vy = vy
        self.w = r_rate

    def __str__(self) -> str:
        """
        formats robot derivative state into string
        """
        return f"vx: {self.vx}, vy: {self.vy}, rot rate: {self.w}"