import numpy as np

# TODO: NEED TO FIX THIS
def Global2Moving(state: np.array) -> np.array:
    """
    rotates vector in the global frame to the moving frame by angle phi
    """
    phi = state[2] # rotation angle

    R = np.array([[np.cos(phi),     np.sin(phi),    0],
                  [-np.sin(phi),    np.cos(phi),    0],
                  [0,               0,              1]])
    
    return np.matmul(R, state)

def Moving2Global(state: np.array) -> np.array:
    """
    @brief  -> transforms vector from moving frame to global frame
    @input state
    """
    phi = -state[2] # rotation angle

    R = np.array([[np.cos(phi),     np.sin(phi),    0],
                  [-np.sin(phi),    np.cos(phi),    0],
                  [0,               0,              1]])
    
    return np.matmul(R, state)