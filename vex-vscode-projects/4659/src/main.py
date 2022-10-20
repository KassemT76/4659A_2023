# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       super                                                        #
# 	Created:      2022-10-19, 3:46:18 p.m.                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

#DEFINING CONTROLLERS AND MOTORS
Controller1 = Controller()
#NUMBER IN BRACKETS IS PORT
motor1 = Motor(4)
motor2 = Motor(5)
motor3 = Motor(10)
motor4 = Motor(9)

#ASSIGNING THE MOTORS TO THE CORRECT GROUPS
motorsLeft = MotorGroup(motor1, motor2)
motorsRight = MotorGroup(motor3, motor4)

#TESTING PRINT
brain.screen.print("Program Loaded!")

#IS CALLED WHEN AXIS2 (RIGHT JOYSTICK - VERTICAL) IS CHANGED
def axisChanged2():
    #DEFINE POSITION OF CONTROLLER JOYSTICK
    pos = Controller1.axis2.position()
    #WHEN POS IS < 0 IT IS POINTING DOWN AND WE MOVE REVERSE
    if pos < 0:
        motorsRight.spin(REVERSE)
        motorsRight.set_velocity(pos, PERCENT)
    else:
        motorsRight.spin(FORWARD)
        motorsRight.set_velocity(pos, PERCENT)

#IS CALLED WHEN AXIS3 (LEFT JOYSTICK - VERTICAL) IS CHANGED
def axisChanged3():
    #DEFINE POSITION OF CONTROLLER JOYSTICK
    pos1 = Controller1.axis3.position()
    #WHEN POS IS < 0 IT IS POINTING DOWN AND WE MOVE REVERSE
    if pos1 < 0:
        motorsLeft.spin(REVERSE)
        motorsLeft.set_velocity(pos1, PERCENT)
        brain.screen.print("Moving reverse left")
    else:
        motorsLeft.spin(FORWARD)
        motorsLeft.set_velocity(pos1, PERCENT)

#LISTENS FOR A CHANGE IN JOYSTICKS
Controller1.axis3.changed(axisChanged3)

Controller1.axis2.changed(axisChanged2)

