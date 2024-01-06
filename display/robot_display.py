"""
Author: Miguel Tamayo

robot_display.py
Contains class for PyQt5 GraphicsItem in charge or drawing the robot
"""

import typing
from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import (QGraphicsItem)
from PyQt5.QtCore import (Qt, QPoint, QPointF, QRectF)

from PyQt5.QtGui import (QPainter, QColor, QPen, QPolygon, QBrush, QPolygonF, QTransform)
import pyqtgraph

import numpy as np

from utilities.constants import *
from utilities.rotations import Cartesian2Pixel
import time

meters_to_pixel = 1

class RobotDisplay(QGraphicsItem):
    """
    Class representing PyQt5 QGraphics widget
    
    inputs:
    -------
        origin_phi: robot's starting heading
        origin_x: robot's starting x position
        origin_y: robot's starting y position
    
    return:
    -------
        display (RobotDisplay): PyQt5 QGraphicsItem object
    """
    def __init__(self,
                 origin_phi = 0,
                 origin_x = 0,
                 origin_y = 0,
                 parent = None,) -> None:
        super().__init__(parent)

        self.painter = QPainter()
        self.x_pos = origin_x # robot's position in the x-axis [cm]
        self.y_pos = origin_y # robot's position in the y-axis [cm]
        self.heading = origin_phi # robot's heading [rad]
        self.robot = QPolygonF()

        # robot item with initial vertix locations. This will be updated throughout the simulation
        self.updatePosition(self.x_pos, self.y_pos, self.heading)

    def updateRobot(self):
        """
        uUpdate self.robot object with new vertices given new self.x and self.y position
        robot's initial heading is facing towards x+ heading is positive counter-clockwise
        
        1. create vertices with heading rotation at the origin of the canvas
        2. translate the robot drawing to the desired position
        """
        # rotate the heading to the graphics frame
        self.heading = -self.heading
        # top left point
        point1 = QPointF((-robot_size/2)*np.cos(self.heading) - (-robot_size/2)*np.sin(self.heading) + self.x_pos,
                         (-robot_size/2)*np.sin(self.heading) + (-robot_size/2)*np.cos(self.heading) + self.y_pos)
        point2 = QPointF((robot_size/2)*np.cos(self.heading) - (-robot_size/2)*np.sin(self.heading) + self.x_pos,
                         (robot_size/2)*np.sin(self.heading) + (-robot_size/2)*np.cos(self.heading) + self.y_pos)
        point3 = QPointF((robot_size/2 + front_size)*np.cos(self.heading) - np.sin(self.heading) + self.x_pos,
                         (robot_size/2 + front_size)*np.sin(self.heading) + np.cos(self.heading) + self.y_pos)
        point4 = QPointF((robot_size/2)*np.cos(self.heading) - (robot_size/2)*np.sin(self.heading) + self.x_pos,
                         (robot_size/2)*np.sin(self.heading) + (robot_size/2)*np.cos(self.heading) + self.y_pos)
        point5 = QPointF((-robot_size/2)*np.cos(self.heading) - (robot_size/2)*np.sin(self.heading) + self.x_pos,
                         (-robot_size/2)*np.sin(self.heading) + (robot_size/2)*np.cos(self.heading) + self.y_pos)
        
        self.robot = QPolygonF([point1, point2, point3, point4, point5])
        self.update()

    def boundingRect(self) -> QRectF:
        """
        returns the rectangle that bounds the robot's shape

        return:
        -------
            bounding_rect (QRectF): robot's bounding rect
        """
        return self.robot.boundingRect()
    
    def paint(self, painter: QPainter, option, widget) -> None:
        """
        draws the robot's polygon

        inputs:
        -------
            painter (Qpainter): painter object in charge of the robot
        """ 
        # draw the custom polygon
        color = QColor(robot_color)
        painter.setBrush(QBrush(color))
        painter.drawPolygon(self.robot)

        return None
    
    def updatePosition(self, x: float, y: float, phi: float) -> None:
        """
        updates the robot's coordinates on the screen

        inputs:
        -------
            x: new x position
            y: new y position
            phi: new heading
        """
        # update the position coordinates and heading
        self.x_pos, self.y_pos = Cartesian2Pixel(x, y)

        # multiply to convert meters to our pixel ratio
        self.x_pos = self.x_pos * m2x 
        self.y_pos = self.y_pos * m2x
        self.heading = phi

        self.updateRobot() # update robot's position
        
        return None
