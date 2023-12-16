"""
states_test.py

File tests functionality of the states.py objects
"""
import sys
sys.path.append("..")

from model.states import *

### creating empty states (0) ###
print("### testing 0.0 states ###")
zero_state = RobotState()
zero_d_state = RobotDerivativeState()

print("state: ", zero_state)
print("derivative state: ", zero_d_state)
print("\n")

### creating non-empty states ###
print("### testing non-0.0 states ###")
state = RobotState(px=1.0, py=2.0, phi=5.0)
d_state = RobotDerivativeState(vx=1, vy=2, r_rate=3)

print("state: ", state)
print("derivative state: ", d_state)
