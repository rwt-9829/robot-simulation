"""
Author: Miguel Tamayo

button.py
contains class for PyQt5 button widget
"""
import typing
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QSlider, QVBoxLayout, QPushButton

class Button(QPushButton):
    """
    creates a PyQt5 button widget

    @input txt (str)    -> text that will display on the button
    @input width (int)  -> button width

    @return None
    """
    buttonClickedSignal = pyqtSignal()
    def __init__(self,
                 txt: str,
                 width: int) -> None:
        super().__init__(parent=None)

        self.setFixedWidth(width) # set the width of the button
        self.setText(txt) # set the text displayed on the button
        self.clicked.connect(self.button_clicked) # connect the button to a function

    def button_clicked(self) -> None:
        """
        emits a buttonClickedSignal signal when this button has been clicked

        @input None

        @return none
        """
        self.buttonClickedSignal.emit()