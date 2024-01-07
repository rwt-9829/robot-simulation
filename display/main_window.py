"""
Author: Miguel Tamayo

main_window.py
Manages all the widgets on the user interface as well as the functions for interactive widgets
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QGraphicsView,
                             QGraphicsScene, QHBoxLayout, QVBoxLayout)

from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QTimer, QRectF, QRect

import numpy as np

from .robot_display import RobotDisplay
from .plotter import Plotter
from .slider import Slider
from .button import Button
from .robot_simulate import RobotSimulate
from inputs.control_inputs import ControlInputs
from utilities.constants import *

from PyQt5.QtWidgets import QWidget

class MainWindow(QMainWindow):
    """
    Class representing PyQt5 window
    
    return:
    -------
        window (MainWindow): PyQt5 window object
    """
    def __init__(self) -> None:
        super().__init__()
        self.robot_simulation = RobotSimulate() # create an instance of the robot's simulation
        self.setWindowTitle("Robot Simulation")

        self.simulationPaused = True # begin with a paused simulation

        ### ----- pyqt5 application window ----- ###
        self.setGeometry(100, 100, window_width, window_height)

        ### ----- main widget ----- ###
        # this is the widget that takes the entire screen and is split in cells
        mainWdiget = QWidget()
        layout = QGridLayout()
        self.setCentralWidget(mainWdiget)

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
        # create button area
        button_layout = QHBoxLayout()
        button_widget = QWidget()

        # create buttons and connect them to their functions
        self.play_button = Button(txt="Play", width=button_width)
        self.play_button.buttonClickedSignal.connect(self.playSimulation)

        self.pause_button = Button(txt="Pause", width=button_width)
        self.pause_button.buttonClickedSignal.connect(self.pauseSimulation)

        self.reset_button = Button(txt="Reset", width=button_width)
        self.reset_button.buttonClickedSignal.connect(self.resetSimulation)

        # add the button objects to the button area
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)

        button_widget.setLayout(button_layout)

        ### ----- control sliders ----- ###
        # create sliders area
        control_sliders_widget = QWidget()
        control_sliders_layout = QVBoxLayout()

        # create slider widgets
        self.vr_slider = Slider(label= "Right Wheel Velocity",
                           min_val=vmin, max_val=vmax,
                           width=int(canvas_width/3), init_val= 0)
        self.vl_slider = Slider(label= "Left Wheel Velocity",
                           min_val=vmin, max_val=vmax,
                           width=int(canvas_width/3), init_val= 0)

        # add the sliders to the slider area
        control_sliders_layout.addWidget(self.vl_slider)
        control_sliders_layout.addWidget(self.vr_slider)
        control_sliders_widget.setLayout(control_sliders_layout)

        ### ----- position graphs ----- ###
        # create graph area
        pos_graph_widget = QWidget()
        pos_graph_layout = QHBoxLayout()

        # create graph objects
        self.x_pos_plot = Plotter(title= "x-axis position", x_label="time (s)", y_label="position (m)")
        self.y_pos_plot = Plotter(title="y-axis position", x_label="time (s)", y_label="position (m)")

        # add the grapsh to the graph area
        pos_graph_layout.addWidget(self.x_pos_plot)
        pos_graph_layout.addWidget(self.y_pos_plot)
        pos_graph_widget.setLayout(pos_graph_layout)

        ### ----- velocity graphs ----- ###
        vel_graph_widget = QWidget()
        vel_graph_layout = QHBoxLayout()

        self.x_vel_plot = Plotter(title="x-axis velocity", x_label="time (s)", y_label="velocity (m/s)")
        self.y_vel_plot = Plotter(title="y-axis velocity", x_label="time (s)", y_label="velocity (m/s)")

        vel_graph_layout.addWidget(self.x_vel_plot)
        vel_graph_layout.addWidget(self.y_vel_plot)
        vel_graph_widget.setLayout(vel_graph_layout)
        
        ### ----- Add widgets to the main layout ----- ###
        # row | column | rowSpan | ColumnSpan
        layout.addWidget(canvas, 0, 0, 2, 1)
        layout.addWidget(button_widget, 2, 0, 1, 1)
        layout.addWidget(control_sliders_widget, 3, 0, 1, 1)
        layout.addWidget(pos_graph_widget, 0, 1, 1, 1)
        layout.addWidget(vel_graph_widget, 1, 1, 1, 1)

        layout.setSpacing(0)
        layout.setRowStretch(3, 2)
        mainWdiget.setLayout(layout)

        ### ----- Simulation Timer ----- ###
        # internal timer that advances simulation on every tick
        self.simulationTimedThread = QTimer()
        self.simulationTimedThread.timeout.connect(self.runSimulation)
        self.time = 0.0

    def runSimulation(self):
        """
        Internal method called in a thread to handle simulation updates
        """
        self.time += dt # advance time
        inputs = ControlInputs(vl=self.vl_slider.get_slider_value(), vr=self.vr_slider.get_slider_value()) # create inputs for robot
        self.robot_simulation.takeStep(inputs) # advance robot in time
        
        # update the robot
        robot_state = self.robot_simulation.getVehicleState()
        robot_dot = self.robot_simulation.getVehicleDotState()
        self.robot.updatePosition(robot_state.px, robot_state.py, robot_state.phi)

        # update plots
        self.x_pos_plot.update_plot_signal.emit(self.time, [robot_state.px])
        self.y_pos_plot.update_plot_signal.emit(self.time, [robot_state.py])
        self.x_vel_plot.update_plot_signal.emit(self.time, [robot_dot.vx])
        self.y_vel_plot.update_plot_signal.emit(self.time, [robot_dot.vy])

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
        Pauses simulation if currently playing
        """
        self.play_button.setDisabled(False)
        self.pause_button.setDisabled(True)
        self.simulationPaused = True
        self.simulationTimedThread.stop()

    def resetSimulation(self):
        """
        Stops and resets the simulation
        """
        self.pauseSimulation() # pause the simulation

        self.time = 0 # reset the simulation time

        # reset the robot drawing
        self.robot_simulation.reset()
        robot_state = self.robot_simulation.getVehicleState()
        self.scene.removeItem(self.robot)
        self.scene.addItem(self.robot)
        self.robot.updatePosition(robot_state.px, robot_state.py, robot_state.phi)

        # reset the plots
        self.x_pos_plot.reset_plot()
        self.y_pos_plot.reset_plot()
        self.x_vel_plot.reset_plot()
        self.y_vel_plot.reset_plot()

        # reset sliders
        self.vl_slider.reset_slider()
        self.vr_slider.reset_slider()

