from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from utilities.constants import *

import pyqtgraph as pg

class Plotter(pg.PlotWidget):
    """
    creates a pyqtgraph plot widget
    """
    update_plot_signal = pyqtSignal(float, float)
    def __init__(self,
                 title: str,
                 x_label: str,
                 y_label: str,
                 legend: str=None) -> None:
        super().__init__(parent=None)

        self.time = []
        self.data = []

        # figure attributes
        self.setBackground(plot_white)
        
        # plot attributes 
        self.plot_item = self.getPlotItem()

        self.plot_item.setTitle(title, color=plot_black)

        self.plot_item.setLabel(axis='bottom', text=x_label, color=plot_white)
        self.plot_item.setLabel(axis='left', text=y_label, color=plot_black)

        self.plot_item.showGrid(x=True, y=True)

        self.plot_item.getAxis('bottom').setTextPen('k')
        self.plot_item.getAxis('left').setTextPen('k')


        self.update_plot_signal.connect(self.update_plot)

    def update_plot(self, time: float, new_data:float) -> None:
        self.time.append(time)
        self.data.append(new_data)
        self.getPlotItem().plot().setData(self.time, self.data, pen=pg.mkPen('b'))

