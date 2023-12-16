import typing
from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPoint

from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon, QBrush
import pyqtgraph

import numpy as np

class RobotStats(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.position_label = QLabel("Robot Position: (0, 0)")
        layout = QVBoxLayout()
        layout.addWidget(self.position_label)
        self.setLayout(layout)