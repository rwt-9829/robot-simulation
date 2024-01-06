"""
Author: Miguel Tamayo

robot_simulate.py
Handles all aspects of the robot's simulation such as updating its position
"""

from model.robot_dynamics import RobotDynamics
from model.states import RobotState, RobotDerivativeState
from inputs.control_inputs import ControlInputs
from utilities.constants import *

class RobotSimulate:
    """
    Wrapper class that handles the robot's dynamics, states, and advancing the robot in time

    return:
    -------
        robot_sim (RobotSimulate): Robot simulation instance
    """
    def __init__(self) -> None:
        self.dt = dt # time steps
        self.time = 0. # initialize simulation time to 0
        self.robot_model = RobotDynamics(dt=self.dt)

    def getVehicleState(self) -> RobotState:
        """
        gets the robot's state

        return:
        -------
            state (RobotState): robot's state
        """
        return self.robot_model.getState()

    def getVehicleDotState(self) -> RobotDerivativeState:
        """
        gets the robot's derivative state
        
        return:
        -------
            dot state (RobotDerivativeState): robot's derivative state
        """
        return self.robot_model.getDotState()
    
    def takeStep(self, controls: ControlInputs) -> None:
        """
        advances the robot (through its dynamics) in time

        inputs:
        -------
            controls (ControlInputs): robot's left and rigth wheel velocities
        """
        self.time += self.dt # step in time
        self.robot_model.update(controls) # update robot state

        return None
    
    def reset(self) -> None:
        """
        resets the robot's states
        """
        self.time = 0.
        self.robot_model.reset()