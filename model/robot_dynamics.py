from .states import RobotState, RobotDerivativeState
from inputs.control_inputs import ControlInputs
from utilities.constants import *

import numpy as np

class RobotDynamics:
    def __init__(self, dt=0.01) -> None:
        self.state = RobotState()           # initialize current robot state to 0
        self.dot = RobotDerivativeState()   # initialize current robot derivative to 0
        self.dt = dt                        # sampling time

    def setState(self, state:RobotState) -> None:
        """
        @brief          -> sets state to desired state
        @param state:   -> robot state
        """
        self.state = state

    def setDotState(self, dot:RobotDerivativeState) -> None:
        """
        @brief  -> sets derivative state to desired derivative state
        @param dot  -> robot's derivative state
        """
        self.dot = dot

    def reset(self):
        """
        @brief  -> makes the robot's state and derivative state both zero
        """
        self.setState(RobotState()) # reset state
        self.setDotState(RobotDerivativeState()) # reset derivative state

    def getState(self) -> RobotState:
        """
        @brief  -> robot's current state getter
        @return -> robot's state
        """
        return self.state
    
    def getDotState(self) -> RobotDerivativeState:
        """
        @brief  -> robot's current derivative state getter
        @return -> robot's derivative state
        """
        return self.dot
    
    def update(self, controls: ControlInputs) -> None:
        self.dot = self.computeDerivative(self.state, controls.vl, controls.vr) # calculate new derivative
        self.state = self.integrateState(self.dt, self.state, self.dot) # integrate by dT
        
        return

    def computeDerivative(self, state: RobotState, vl: float, vr: float) -> RobotDerivativeState:
        """
        @brief  -> computes the robot's time-derivative given the linear velocities in the
                    robot's local frame
        @param phi  -> robot's heading (rad)
        @param vl   -> left wheel's linear velocity input (cm/s)
        @param vr   -> right wheel's linear velocity input (cm/s)
        @return -> time derivative state
        """
        dot = RobotDerivativeState() # empty state
        v = (vr + vl) / 2. # robot's linear velocity in robot's frame
        w = (vr - vl) / L # robot's angular velocity around center

        # create derivative state
        dot.vx = v * np.cos(state.phi + (w*self.dt)/2) # vel in global frame
        dot.vy = v * np.sin(state.phi + (w*self.dt)/2) # vel in global frame
        dot.w = w

        return dot
    
    def integrateState(self, dT: float, state: RobotState, dot: RobotDerivativeState) -> RobotState:
        """
        @brief -> Integrates the vehicle state using trapezoidal integration
        @param: dT -> sampling time [s]
        @param: state -> robot state to integrate
        @param: dot -> robot derivative state
        @return: new_state -> new robot state with integrated components
        """

        new_state = RobotState() # create empty instance
        new_state.px = state.px + dot.vx * dT
        new_state.py = state.py + dot.vy * dT
        new_state.phi = state.phi + dot.w * dT

        return new_state



