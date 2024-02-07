"""
Author: Miguel Tamayo

robot_simulate.py
Handles all aspects of the robot's simulation such as updating its position
"""

from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from model.robot_kinematics import RobotKinematics
from model.states import RobotState, RobotDerivativeState
from inputs.control_inputs import WheelLinearInputs
from utilities.constants import *

class RobotSimulate1(QObject):
    # sends the robot's state when calculations are finished
    finished_signal = pyqtSignal(RobotState)

    stop_signal = pyqtSignal() # signal to stop the internal timer
    start_signal = pyqtSignal() # signal to start the internal timer

    # sends parameters necessary to update the plots
    update_plots_signal = pyqtSignal(float, RobotState, RobotDerivativeState)

    def __init__(self) -> None:
        super().__init__(parent=None)
        self.dt = dt # time steps
        self.time = 0. # initialize simulation time ot 0
        self.robot_model = RobotKinematics(dt=self.dt)
        self.ticks = 0

        # setup the timer for the object
        self.simulationTimedThread = QTimer()
        self.simulationTimedThread.timeout.connect(self.takeStep)

        # connect the signals to start and stop the simulation
        self.start_signal.connect(self.run)
        self.stop_signal.connect(self.stop)
        

    def run(self) -> None:
        """
        runs the timer for the main robot updates on this new thread
        """
        self.simulationTimedThread.start(10)

    def stop(self) -> None:
        """
        stops the internal simulation timer
        """
        self.simulationTimedThread.stop()

    def takeStep(self) -> None:
        """
        advances the robot (through its kinematics) in time
        """
        self.ticks += 1
        self.time += self.dt # step in time
        inputs = WheelLinearInputs(vl=0.4, vr=0.5)
        self.robot_model.update(inputs) # update robot state

        self.finished_signal.emit(self.robot_model.getState()) # emit a signal to tell we're done

        if self.ticks % plotUpdateTicks == 0:
            self.update_plots_signal.emit(self.time, self.robot_model.getState(), self.robot_model.getWheelVelocities())

        return None
    
    def getStates(self) -> list:
        """
        returns the different states of interest from the robot
        """

        return self.robot_model.getState(), self.robot_model.getWheelVelocities()

    def reset(self) -> None:
        """
        resets the robot's states
        """
        self.time = 0.
        self.robot_model.reset() 

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
        self.robot_model = RobotKinematics(dt=self.dt)
    
    def takeStep(self, controls: WheelLinearInputs) -> None:
        """
        advances the robot (through its dynamics) in time

        inputs:
        -------
            controls (WheelLinearInputs): robot's left and rigth wheel velocities
        """
        self.time += self.dt # step in time
        self.robot_model.update(controls) # update robot state

        return None
    
