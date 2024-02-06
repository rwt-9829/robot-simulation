"""
Author: Miguel Tamayo

main_window.py
Manages all the widgets on the user interface as well as the functions for interactive widgets
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QGridLayout, QGraphicsView,
                             QGraphicsScene, QHBoxLayout)

from PyQt5.QtCore import QThread, QMetaObject

import numpy as np

from .robot_display import RobotDisplay
from .path import Path
from .plotter import Plotter
from .button import Button
from model.states import RobotState, RobotDerivativeState
from .robot_simulate import RobotSimulate, RobotSimulate1
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
        self.robot_path = Path(line_color, 1.5) # path to follow robot's position

        # add robot and path to the scene
        self.scene.addItem(self.robot)
        self.scene.addItem(self.robot_path)

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

        ### ----- state graphs ----- ###
        # create graph area
        state_graph_widget = QWidget()
        state_graph_layout = QHBoxLayout()

        # create graph objects
        self.x_pos_plot = Plotter(title= "x-axis position", x_label="time (s)", y_label="position (m)")
        self.y_pos_plot = Plotter(title="y-axis position", x_label="time (s)", y_label="position (m)")
        self.phi_plot = Plotter(title="heading", x_label="time (s)", y_label="heading (deg)")

        # add the grapsh to the graph area
        state_graph_layout.addWidget(self.x_pos_plot)
        state_graph_layout.addWidget(self.y_pos_plot)
        state_graph_layout.addWidget(self.phi_plot)
        state_graph_widget.setLayout(state_graph_layout)

        ### ----- velocity graphs ----- ###
        vel_graph_widget = QWidget()
        vel_graph_layout = QHBoxLayout()

        self.vl_plot = Plotter(title="left wheel linear vel", x_label="time (s)", y_label="velocity (m/s)")
        self.vr_plot = Plotter(title="right wheel linear vel", x_label="time (s)", y_label="velocity (m/s)")

        vel_graph_layout.addWidget(self.vl_plot)
        vel_graph_layout.addWidget(self.vr_plot)
        vel_graph_widget.setLayout(vel_graph_layout)
        
        ### ----- Add widgets to the main layout ----- ###
        # row | column | rowSpan | ColumnSpan
        layout.addWidget(canvas, 0, 0, 2, 1)
        layout.addWidget(button_widget, 2, 0, 1, 1)
        layout.addWidget(state_graph_widget, 0, 1, 1, 1)
        layout.addWidget(vel_graph_widget, 1, 1, 1, 1)

        layout.setSpacing(0)
        layout.setRowStretch(3, 2)
        mainWdiget.setLayout(layout)

        ### ----- Simulation Thread ----- ###
        self.sim_thread = QThread() # create thread for simulation
        self.robot_sim = RobotSimulate1() # create simulation object
        self.robot_sim.moveToThread(self.sim_thread) # move object into thread

        # connect thread signals
        self.sim_thread.started.connect(self.robot_sim.start_signal.emit)
        self.sim_thread.finished.connect(self.robot_sim.stop_signal.emit)
        self.robot_sim.finished_signal.connect(self.updateGUI)
        self.robot_sim.update_plots_signal.connect(self.updatePlots)

    def updateGUI(self, robot_state: RobotState) -> None:
        """
        Updates the canvas and graphs
        """
        self.robot_path.updatePath(robot_state.px, robot_state.py)
        self.robot.updatePosition(robot_state.px, robot_state.py, robot_state.phi)

    def updatePlots(self, time: float, state: RobotState, wheel_vel: RobotDerivativeState) -> None:
        """
        Updates GUI graphs
        """
        self.x_pos_plot.update_plot_signal.emit(time, [state.px])
        self.y_pos_plot.update_plot_signal.emit(time, [state.py])
        self.phi_plot.update_plot_signal.emit(time, [np.rad2deg(state.phi)])

        self.vl_plot.update_plot_signal.emit(time, [wheel_vel.vx])
        self.vr_plot.update_plot_signal.emit(time, [wheel_vel.vy])

    def playSimulation(self):
        """
        Starts simulation if currently stopped
        """
        # start thread
        self.sim_thread.start()

        # update button statuses
        self.play_button.setDisabled(True)
        self.pause_button.setDisabled(False)
        self.simulationPaused = False

    def pauseSimulation(self):
        """
        Pauses simulation if currently playing
        """
        self.sim_thread.quit() # stop the thread

        # update the button statues
        self.play_button.setDisabled(False)
        self.pause_button.setDisabled(True)

        self.simulationPaused = True

    def resetSimulation(self):
        """
        Stops and resets the simulation
        """
        self.pauseSimulation() # pause the simulation

        # reset robot object
        self.robot_sim.reset()
        robot_state = self.robot_sim.robot_model.getState()
        self.scene.removeItem(self.robot)
        self.scene.addItem(self.robot)
        self.robot.updatePosition(robot_state.px, robot_state.py, robot_state.phi)

        # reset path object
        self.robot_path.clear_path()

        # reset the plots
        self.x_pos_plot.reset_plot()
        self.y_pos_plot.reset_plot()
        self.phi_plot.reset_plot()
        self.vl_plot.reset_plot()
        self.vr_plot.reset_plot()
