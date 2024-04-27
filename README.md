# 2D Wheeled Robot Dynamics Simulation
## Description
This project aims to simulate a [differential drive robot](https://en.wikipedia.org/wiki/Differential_wheeled_robot) by implementing the kinematics of the vehicle
on a virtual environment.

<img src="https://github.com/miguel-a-tamayo/robot-simulation/assets/83749938/e8be74a1-4ef6-4064-8db3-7247d6e39a29" width="700" height="450">


## Motivation
Even though my background is in Computer Engineering, I enjoy learning about physical machines like robots. I wanted to learn how robots move and insteract with the world
around them. What better way than to build my own simulator?

## Resources
This simulation is currently being built using Python coding language and the [PyQt5](https://pypi.org/project/PyQt5/#:~:text=PyQt5%20is%20a%20comprehensive%20set,platforms%20including%20iOS%20and%20Android.)
framework.

The code I have written comes from the concepts taught in the book *Wheeled Mobile Robotics: From Fundamentals Towards Autonomous Systems*

## Setup
In order to run the simulation you need to install PyQt5 and PyQtGraph. After, follow the next instructions

1. Clone this repository
2. There are currently 2 branches:

   1.`main`: This is used as a testing branch. When play is pressed, the robot will go in a circle

   2.`manual_drive`: This branch allows you to directly input left and right wheel linear velocities and see how the robot steers.


## Next Step
- [ ] Implement heading controller
- [ ] Covert main and manual drive to C++ with windows executable capabilities
- [ ] Wrap heading values to [0 360]

## What I've Learned
* Wheeled robot kinematics
