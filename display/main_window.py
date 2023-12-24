import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QGraphicsView,
                             QGraphicsScene, QGraphicsLineItem, QHBoxLayout)

from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QTimer, QRectF, QRect

import numpy as np

from .robot_display import RobotDisplay
from .plotter import Plotter
from .slider import Slider
from .button import Button
from .robot_simulate import RobotSimulate
from .robot_stats import RobotStats
from inputs.control_inputs import ControlInputs
from utilities.constants import *

from PyQt5.QtWidgets import QWidget

class MainWindow(QMainWindow):
    # updateVehiclePositionSignal = pyqtSignal(list) # signal for redrawing vehicle

    def __init__(self) -> None:
        super().__init__()
        self.robot_simulation = RobotSimulate() # create an instance of the robot's simulation
        self.setWindowTitle("Robot Simulation")

        self.simulationPaused = True

        ### ----- pyqt5 application window ----- ###
        self.setGeometry(100, 100, window_width, window_height)

        ### ----- main widget ----- ###
        # this is the widget that takes the entire screen and is split in cells
        mainWdiget = QWidget()
        layout = QGridLayout()
        self.setCentralWidget(mainWdiget)
        mainWdiget.setLayout(layout)

        ### ----- simulation canvas widget ----- ###
        canvas = QGraphicsView(mainWdiget) # create QGrahicsView object as a viewport to the drawings
        canvas.setFixedSize(canvas_width, canvas_height) # set the canvas size

        # create scene to handle robot item
        self.scene = QGraphicsScene(canvas)
        self.scene.setBackgroundBrush(background_color)
        self.robot = RobotDisplay() # create robot instance at the origin facing x+
        self.scene.addItem(self.robot) # add the robot to the scene

        canvas.setScene(self.scene) # add the scene to the canvas

        ### ----- play, stop, and reset buttons ----- ###
        button_layout = QHBoxLayout()
        button_widget = QWidget()

        self.play_button = Button(txt="Play", width=button_width)
        self.play_button.buttonClickedSignal.connect(self.playSimulation)

        self.pause_button = Button(txt="Pause", width=button_width)
        self.pause_button.buttonClickedSignal.connect(self.pauseSimulation)

        self.reset_button = Button(txt="Reset", width=button_width)
        self.reset_button.buttonClickedSignal.connect(self.resetSimulation)

        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)

        button_widget.setLayout(button_layout)

        ### ----- position graphs ----- ###
        position_graph_widget = QWidget()
        position_graph_layout = QHBoxLayout()

        self.x_pos_plot = Plotter(title= "x-axis position", x_label="time (s)", y_label="position (m)")
        self.y_pos_plot = Plotter(title="y-axis position", x_label="time (s)", y_label="position (m)")

        position_graph_layout.addWidget(self.x_pos_plot)
        position_graph_layout.addWidget(self.y_pos_plot)
        position_graph_widget.setLayout(position_graph_layout)

        ### ----- Add widgets to the main layout ----- ###
        layout.addWidget(canvas, 0, 0)
        layout.addWidget(button_widget, 1, 0)
        layout.addWidget(position_graph_widget, 0, 1)

        ### ----- Simulation Timer ----- ###
        self.simulationTimedThread = QTimer()
        self.simulationTimedThread.timeout.connect(self.runSimulation)
        self.time = 0.0

    def runSimulation(self):
        """
        internal method called in a thread to handle simulation updates
        """
        self.time += dt 
        inputs = ControlInputs(vl=0.4, vr=0.4)
        self.robot_simulation.takeStep(inputs) # advance robot in time
        
        robot_state = self.robot_simulation.getVehicleState()
        robot_dot = self.robot_simulation.getVehicleDotState()
        self.robot.updatePosition(robot_state.px, robot_state.py, robot_state.phi)

    def playSimulation(self):
        """
        Starts simulation if currently stopped
        """
        self.play_button.setDisabled(True)
        self.pause_button.setDisabled(False)
        self.simulationPaused = False
        self.simulationTimedThread.start(10) # start timer at dt (10ms)

    def pauseSimulation(self):
        """
        pauses simulation if currently playing
        """
        self.play_button.setDisabled(False)
        self.pause_button.setDisabled(True)
        self.simulationPaused = True
        self.simulationTimedThread.stop()

    def resetSimulation(self):
        """
        stops and resets the simulation
        """
        self.pauseSimulation() # pause the simulation

        self.time = 0 # reset the simulation time

        # reset the robot drawing
        self.robot_simulation.reset()
        robot_state = self.robot_simulation.getVehicleState()
        self.scene.removeItem(self.robot)
        self.scene.addItem(self.robot)
        self.robot.updatePosition(robot_state.px, robot_state.py, robot_state.phi)
