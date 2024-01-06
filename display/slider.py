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
    internal_max = 100
    internal_min = -100
    def __init__(self,
                 label: str,
                 min_val: int,
                 max_val: int,
                 width: int,
                 init_val: int = 0,
                 orientation: int = 1) -> None:
        super().__init__(parent=None)

        self.init_val = init_val
        self.ratio = (max_val - min_val) / (self.internal_max - self.internal_min)
        self.value = init_val

        layout = QHBoxLayout() # want a horizontal layout

        label = QLabel(label) # slider's label
        self.value_txt = QLabel(f"{init_val}") # slider's value

        # slider and alider attributes
        self.slider = QSlider()
        self.slider.setOrientation(orientation)
        self.slider.setRange(self.internal_min, self.internal_max)
        self.slider.setMaximumWidth(width)

        # add the items to the layout
        layout.addWidget(label)
        layout.addWidget(self.slider)
        layout.addWidget(self.value_txt)

        # set the widget's layout
        self.setLayout(layout)

        self.slider.valueChanged.connect(self.value_changed)

    def value_changed(self, value: int) -> None:
        """
        Changes the displayed value on the slider and emmits a signal for any other outside updates

        inputs:
        -------
            value (int): new slider value 
        """
        mapped_value = float(value) * self.ratio
        self.value = mapped_value
        self.value_txt.setText("{:.2f}".format(mapped_value))
        self.valueChangedSignal.emit()

    def reset_slider(self) -> None:
        """
        Sets slider to the original position
        """
        self.slider.setValue(self.init_val)

    def get_slider_value(self) -> float:
        """
        wrapper function to get the slider's value

        return:
        -------
            value (float): slider's mapped value        
        """

        return float(self.slider.value()) * self.ratio
