"""
Author: Miguel Tamayo

button.py
contains class for PyQt5 button widget
"""
import typing
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QSlider, QVBoxLayout, QPushButton

class Button(QWidget):
    """
    creates a PyQt5 button widget

    @input: txt (str)           -> text that will display on the button
    @input: width (int)         -> button width 
    @input: parent (QWidget)    -> parent widget that will hold the button

    @return: None
    """
    buttonClickedSignal = pyqtSignal()
    def __init__(self,
                 txt: str,
                 width: int,
                 parent: QWidget) -> None:
        super().__init__(parent)

        self.button = QPushButton(txt, parent)
        self.button.setFixedWidth(width)
        self.button.clicked.connect(self.clicked_event)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def clicked_event(self) -> None:
        """
        emits a signal when this button has been clicked 

        @input: None
        
        @return: None
        """
        self.buttonClickedSignal.emit()