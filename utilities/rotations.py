"""
Author: Miguel Tamayo

rotations.py
Holds any function that performs rotations between different frames
"""

import numpy as np

def Cartesian2Pixel(x: float, y:float) -> tuple:
    """
    Converts Cartesian coordinates to Pixel coordinates used by computers
    x-axis remain the same (postive going right) but y-axes are opposite

    inputs:
    -------
        x (float): x coordinate in cartesian frame
        y (float): y coordinate in cartesian frame
    
    return:
    -------
        (x, y) (float) -> pixel frame x and y coordinates
    """

    return (x, -y)