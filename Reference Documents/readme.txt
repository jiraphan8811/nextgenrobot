Project planning
Ref: https://github.com/manojsharma221/Robot-Sketcher-5-bar-parallel-manipulator-?tab=readme-ov-file

Technology use:
- python programming to solve the inverse kinematics equation
- Developed an algorithm to make the robot able to use gcode in python and fill the missing coordinates to maintain desired level of smoothness of lines/curves drawn.
- Developed an algorithm to keep track of the error in the movement of the links occuring due to resolution limitation of the stepper motors and the motor drivers.The algorithm also tries to correct the error with each input coordinate without the use of close loop control(means not encoder senssors necessary). The prevent the accumulation of error and keeps the error in the movement of the end effector minimum.

SOFTWARE REQUIRMENTS
Python 3.6(and for library requirments see "robot_main.py" file)

Arduino IDE

Inkscape for making vector image

For vector to g-code visit: jscut.org