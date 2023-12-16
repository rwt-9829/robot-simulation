"""
File that holds all the constants used throughout the simulation
"""

from PyQt5.QtGui import (QColor)

### ----- Robot Constants ----- ###
# TODO: Need to make the velocities depend on the RPM of the wheel and make the RPM the inputs to sliders
L = .20         # wheel base (distance between both wheels) [m]
wheel_r = 0.03  # wheel radius [m]
scaling_unit = 0.25 # determines the relative size of the front tip
robot_size = 50. # size of sides
front_size = robot_size * scaling_unit

vmax = 20 # wheels max linear velocity [cm/s]
vmin = -vmax 


### ----- Simulation Constants ----- ###
dt = 0.01 # 20ms timer

### ----- Application Constants ----- ###
window_height = 1000
window_width = 1500

canvas_height = 800
canvas_width = 800

### ------ Colors ----- ###
background_color = QColor(57, 57, 57)
robot_color = QColor(200, 200, 200)

