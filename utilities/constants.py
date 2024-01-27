"""
Author: Miguel Tamayo

constants.py
Holds all the constants used throughout the simulation
"""

from PyQt5.QtGui import (QColor)

### ----- plot constants ----- ####
plot_black = (0, 0, 0)
plot_white = (255, 255, 255)
plot_red = (255, 0, 0)
plot_orange = (0.8500, 0.3250, 0.0980)
plot_blue = (66, 138, 245)
plot_grey = (188, 188, 188, 100)

### ----- scaling constants ----- ###
m2x = 100 # meter to pixel

### ----- Robot Constants ----- ###
L = .20         # wheel base (distance between both wheels) [m]
wheel_r = 0.03  # wheel radius [m]
robot_size = 50. # size of robot sides [px]

scaling_unit = 0.25 # determines the relative size of the front tip of the robot
front_size = robot_size * scaling_unit # size of robot's front tip

vmax = 1 # wheels max linear velocity [m/s]
vmin = -vmax 

heading_max = 180
heading_min = -heading_max

### ----- Simulation Constants ----- ###
dt = 0.01 # 10ms timer
plotUpdateTicks = 10

### ----- Application Constants ----- ###
window_height = 1000
window_width = 1500

canvas_height = 800
canvas_width = 800

button_width = int(canvas_width / 3.2)
slider_width = int(canvas_width / 2.5)

### ------ Colors ----- ###
background_color = QColor(57, 57, 57)
robot_color = QColor(161, 217, 139)
line_color = QColor(203, 209, 203)

