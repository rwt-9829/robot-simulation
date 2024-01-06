"""
Author: Miguel Tamayo

slider.py
Contains class for PyQt5 slider widget
"""

import typing
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout, QLabel

class Slider(QWidget):
    """
    Class representing PyQt5 slider widget with labels and values

    inputs:
    -------
        min_val (int): slider's minimum value
        max_val (int): slider's maximum value
        width (int): slider object width
        init_val (int): slider's initial value
        tick_interval (int): sliders ticks
        orientation (int): 1 -> horizontal; 0 -> vertical

    return:
    -------
        slider (Slider): PyQt5 slider widget
    """
    valueChangedSignal = pyqtSignal()
    def __init__(self,
                 label: str,
                 min_val: int,
                 max_val: int,
                 width: int,
                 init_val: int = 0,
                 tick_interval: int = 2,
                 orientation: int = 1) -> None:
        super().__init__(parent=None)

        layout = QHBoxLayout() # want a horizontal layout

        label = QLabel(label) # slider's label
        self.value = QLabel(f"{init_val}") # slider's value

        # slider and alider attributes
        self.slider = QSlider()
        self.slider.setOrientation(orientation)
        self.slider.setRange(min_val, max_val)
        self.slider.setTickInterval(tick_interval)
        self.slider.setMaximumWidth(width)

        # add the items to the layout
        layout.addWidget(label)
        layout.addWidget(self.slider)
        layout.addWidget(self.value)

        # set the widget's layout
        self.setLayout(layout)

        self.slider.valueChanged.connect(self.valueChanged)

    def valueChanged(self, value: int) -> None:
        """
        Changes the displayed value on the slider and emmits a signal for any other outside updates        
        """
        self.value.setText(str(value))
        self.valueChangedSignal.emit()