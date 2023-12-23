import numpy as np

def Cartesian2Pixel(x: float, y:float) -> tuple:
    """
    Converts Cartesian coordinates to Pixel coordinates used by computers
    x-axis remain the same (postive going right) but y-axes are opposite

    @input: x (float) -> x coordinate in cartesian frame
    @input: y (float) -> y coordinate in cartesian frame

    @return (x, y) (float) -> Pixel frame x and y coordinates
    """

    return (x, -y)