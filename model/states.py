import numpy as np

class RobotState:
    def __init__(self,
                 px: float = 0.0,
                 py: float = 0.0,
                 phi: float = 0.0) -> None:
        """
        Defines vehicle states to define the robot's current position.
        Frame: Global

        @param px: initial robot x position in global frame [m]
        @param py: initial robot y position in global frame [m]
        @param phi: initial orientation of robot [rad]
        """
        # state vector
        self.px = px
        self.py = py
        self.phi = phi

    def __str__(self) -> str:
        return f"x: {self.px}, y: {self.py}, heading: {self.phi}"

        
class RobotDerivativeState:
    def __init__(self,
                 local_v = 0.0,
                 vx: float = 0.0,
                 vy: float = 0.0,
                 r_rate: float = 0.0) -> None:
        """
        Defines vehicle derivative state
        Frame: Global

        @param local_v  -> linear velocity in the robot's local frame
        @param vx: robot x velocity in the global frame [m/s]
        @param vy: robot y velocity in the global frame [m/s]
        @param r_rate: robot turning rate [rad/s]
        """

        # derivative state vector
        self.local_v = local_v
        self.vx = vx
        self.vy = vy
        self.w = r_rate

    def __str__(self) -> str:
        return f"vx: {self.vx}, vy: {self.vy}, rot rate: {self.w}"