"""
Author: Miguel Tamayo

slider.py
Contains class for PyQt5 slider widget
"""

import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QSlider, QVBoxLayout

class Slider(QWidget):
    """
    Class representing PyQt5 slider widget
    
    inputs:
    -------
        min_val (int): slider's minimum value
        max_val (int): slider's maximum value
        width (int): slider's object width
        init_val (int): sliders initial value

    return:
    -------
        button (Button): PyQt5 button object
    """
    def __init__(self,
                 min_val: int,
                 max_val: int,
                 width: int,
                 init_val: int = 0,
                 parent=None) -> None:
        super().__init__(parent)

        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(min_val, max_val)
        self.slider.setValue(init_val)
        self.slider.setTickInterval(5)
        self.slider.setMaximumWidth(width)
        # self.slider.

        self.slider.valueChanged.connect(self.valueChanged)

        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        self.setLayout(layout)
    
    def valueChanged(self, value):
        """
        sets the slider's value to what it has been cahnges to

        inputs:
        -------
            value: new slider value
        """
        self.slider.setValue(value)
