import typing
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QSlider, QVBoxLayout, QPushButton

class Button(QWidget):
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

    def clicked_event(self):
        self.buttonClickedSignal.emit()