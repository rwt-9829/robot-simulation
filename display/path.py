"""
Author: Miguel Tamayo

line.py
Contains class to create a path on the canvas
"""

from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtGui import QColor, QPen, QPainterPath
import numpy as np

from utilities.rotations import *
from utilities.constants import *

class Path(QGraphicsPathItem):
    """
    Class creates QGraphicsPathItem to track objects on the canvas
    
    inputs:
    -------
    
    return:
    -------
        Path (QGraphicsPathItem): PyQt5 QGraphicsPathItem object
    """
    def __init__(self,
                 color: QColor,
                 width: 1,
                 parent=None) -> None:
        super().__init__(parent)

        pen = QPen(color, width)
        self.setPen(pen)

    def updatePath(self, x:float, y:float) -> None:
        """
        Adds new coorinates to the path and updates the path item

        inputs:
        -------
            x (float): new x-axis coordinate
            y (float): new y-axis coordinate
        """
        
        new_points = Cartesian2Pixel([[x, y]])
        x = new_points[0][0]
        y = new_points[0][1]

        path = QPainterPath(self.path())
        path.lineTo(x * m2x, y * m2x)
        self.setPath(path)

        return None

    def clear_path(self) -> None:
        """
        Removes points that were in the path
        """

        path = QPainterPath(self.path())
        path.clear()
        self.setPath(path)