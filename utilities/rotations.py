"""
Author: Miguel Tamayo

rotations.py
Holds any function that performs rotations between different frames
"""

import numpy as np

def Cartesian2Pixel(points: list[list[float]]) -> list[list[float]]:
    """
    Converts Cartesian coordinates to Pixel coordinates used by computer
    x-axis remain the same (postive going right) but y-axes are opposite

    inputs:
    -------
        points (list[list[float]]): points in cartesian frame
    
    return:
    -------
        converted_points (list[list[float]]): points in pixel frame
    """

    return [[point[0], -point[1]] for point in points]

def rotation_matrix(phi: float) -> list[list[float]]:
    """
    creates a 2-D matrix to rotate vertices in the cartesian frame

    inputs:
    -------
        phi (float): angle between x-axis and vehicle's body frame x-axis

    output:
    -------
        matrix (list[list[float]])
    """

    matrix = [[np.cos(phi), np.sin(phi)],
              [-np.sin(phi), np.cos(phi)]]

    return matrix

def offset(vertices: list[list[float]], x: float, y: float) -> list[list[float]]:
    """
    offsets each x, y point in the vertix by the respective x and y offset

    inputs:
    -------
        vertices (list[list[float]]): vertices describing object polygon
        x (float): x-axis offset
        y (float): y-axis offset

    output:
    -------
        matrix (list[list[float]]): new matrix with applied offsets
    """

    return [[point[0] + x, point[1] + y] for point in vertices]