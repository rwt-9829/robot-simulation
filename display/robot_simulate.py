"""
Author: Miguel Tamayo
date: 09/09/2023

robot_simulate.py   -> handles all aspects of the robot's simulation such as updating its position
"""

from model.robot_dynamics import RobotDynamics
from inputs.control_inputs import ControlInputs
from utilities.constants import *

class RobotSimulate:
    def __init__(self) -> None:
        self.dt = dt # time steps
        self.time = 0. # initialize simulation time to 0
        self.robot_model = RobotDynamics(dt=self.dt)

    def getVehicleState(self):
        return self.robot_model.getState()

    def getVehicleDotState(self):
        return self.robot_model.getDotState()
    
    def takeStep(self, controls: ControlInputs):
        self.time += self.dt # step in time
        self.robot_model.update(controls) # update robot state

        return
    
    def reset(self):
        self.time = 0.
        self.robot_model.reset()

