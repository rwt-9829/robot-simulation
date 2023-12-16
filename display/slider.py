import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QSlider, QVBoxLayout

class Slider(QWidget):
    def __init__(self,
                #  label,
                 min_val,
                 max_val,
                 width,
                 init_val = 0,
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
        self.slider.setValue(value)
