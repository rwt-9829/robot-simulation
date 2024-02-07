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

import numpy as np

from utilities.constants import *
from utilities.rotations import *

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

        # vehicle vertices
        # defined with vehicle facing +x
        #|---\
        #|---/
        # [x, y] points
        self.vertices = [[-robot_size/2, robot_size/2], # top left
                         [robot_size/2, robot_size/2],  # top right
                         [robot_size/2 + front_size, 0], # front
                         [robot_size/2, -robot_size/2], # bottom right
                         [-robot_size/2, -robot_size/2]] # bottom left

        # robot item with initial vertix locations. This will be updated throughout the simulation
        self.updatePosition(self.x_pos, self.y_pos, self.heading)

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
            x (float): cartesian x offset
            y (float): cartesian y offset
            phi (float): heading
        """

        new_points = self.vertices # get the vertices at the origin
        rot_matrix = rotation_matrix(phi= phi)

        # rotate and offset vertices
        new_points = np.matmul(new_points, rot_matrix)
        new_points = offset(new_points, x * m2x, y * m2x)

        # offset vertices
        new_points = Cartesian2Pixel(new_points)

        self.robot = QPolygonF([QPointF(point[0], point[1]) for point in new_points]) # create new robot object
        self.update()
        
        return None
