"""
Author: Miguel Tamayo

plotter.py
Contains class for PyQtGraph widget
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from utilities.constants import *

import pyqtgraph as pg

class Plotter(pg.PlotWidget):
    """
    Class representing PyQtGraph plot widget
    
    inputs:
    -------
        title (str): plot title
        x_label (str): x-axis label
        y_label (str): y-axis label
        num_plots (int): number of lines to be drawn on the plot
        legends (list): list of legend names for lines

    return:
    -------
        plot (Plotter): PyQtGraph plot object
    """
    update_plot_signal = pyqtSignal(float, list) # signal that will trigger a plot update
    def __init__(self,
                 title: str,
                 x_label: str,
                 y_label: str,
                 num_plots: int=1,
                 legends: list=None) -> None:
        super().__init__(parent=None)

        self.line_colors = [plot_blue, plot_red, plot_orange]
        self.time = []
        self.data_sets = []
        self.plot_lines = []
        num_plots
        legends

        # figure attributes
        self.setBackground(plot_white)
        self.setFixedSize(275, 350)
        
        # plot attributes 
        self.plot_item = self.getPlotItem()

        self.plot_item.setTitle(title, color=plot_black)

        self.plot_item.setLabel(axis='bottom', text=x_label, color=plot_white)
        self.plot_item.setLabel(axis='left', text=y_label, color=plot_black)

        self.plot_item.showGrid(x=True, y=True)

        self.plot_item.getAxis('bottom').setTextPen('k')
        self.plot_item.getAxis('left').setTextPen('k')

        if legends is not None:
            self.plot_item.addLegend(labelTextColor=plot_black, brush=plot_grey)

        # iterate over the number of lines and add a plot instance
        for idx in range(num_plots): 
            self.data_sets.append([]) # append a list for this line set
            if legends is not None:
                self.plot_lines.append(self.plot_item.plot(name=legends[idx], pen=pg.mkPen(self.line_colors[idx])))
            else:
                self.plot_lines.append(self.plot_item.plot(pen=pg.mkPen(self.line_colors[idx])))

        self.update_plot_signal.connect(self.update_plot)

    def update_plot(self, time: float, new_data:list) -> None:
        """
        Adds new data to the plot

        inputs:
        -------
            time (float): x-axis value
            new_data (list): y-axis values for each line to be plotted
        """
        self.time.append(time) # add time point

        for data_set, plot_line, data_point in zip(self.data_sets, self.plot_lines, new_data):
            data_set.append(data_point) # append the data to its corresponding list
            plot_line.setData(self.time, data_set) # update the plot

        return None

    def reset_plot(self) -> None:
        """
        Clears all the plots and erases the sotred data
        """
        self.time.clear() # clear time list
        for data_set, plot_line in zip(self.data_sets, self.plot_lines):
            data_set.clear()
            plot_line.setData(self.time, data_set)

        return None