"""
robot_dynamics_test.py

File tests the functions that describe the dynamics of the robot
"""

import sys
sys.path.append("..")

from model.robot_kinematics   import RobotKinematics
from inputs.control_inputs  import ControlInputs
from model.states           import RobotState, RobotDerivativeState

import matplotlib.pyplot as plt
import numpy as np

dynamics = RobotKinematics()
expected = RobotKinematics()

### Testing derivative states ###
inputs = ControlInputs(10, 10)
expected.setDotState(RobotDerivativeState(vx=10.0, vy=0.0, r_rate=0.0))
print('Initial derivative state: ', dynamics.getDotState())
print('~~~ Inserting inputs ~~~')
dynamics.setDotState(dynamics.computeDerivative(dynamics.getState().phi, inputs.vl, inputs.vr))
print('Expected derivative state: ', expected.getDotState())
print('Actual derivative state: ', dynamics.getDotState())

### Testing derivative with changing heading ###
dynamics.reset() # reset for new test
print('This test will generate a graph with the dynamics states and derivatives')
print('If correct, velocities should show as sinusoidal waves')

dt = 0.01
time = np.arange(0, 1000, dt)
vx = np.zeros(shape=np.shape(time))
x = np.zeros(shape=np.shape(time))
y = np.zeros(shape=np.shape(time))
vy = np.zeros(shape=np.shape(time))
phi = np.zeros(shape=np.shape(time))
inputs = ControlInputs(vl=1, vr=0)

for i in range(1, len(time)):
    dynamics.update(inputs) # update the states
    dot = dynamics.getDotState()
    state = dynamics.getState()

    vx[i] = dot.vx
    vy[i] = dot.vy
    x[i] = state.px
    y[i] = state.py
    phi[i] = state.phi

# plot the data
plt.suptitle("changing heading result")
plt.subplot(2, 2, 1)
plt.plot(time, vx)
plt.title('x-velocity')
plt.ylabel('velocity [m/s]')

plt.subplot(2, 2, 2)
plt.plot(time, vy)
plt.title('y-velocity')

plt.subplot(2, 2, 3)
plt.plot(time, x)
plt.title('x-position')

plt.subplot(2, 2, 4)
plt.plot(time, y)
plt.title('y-position')

plt.show()

# plt.subplot(2, 1, 2)
# plt.plot(time, vy)
# plt.ylabel('y-velocity')

# plt.xlabel('Time (s)')
# plt.grid(True)
# plt.show()