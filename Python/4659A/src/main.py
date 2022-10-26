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
Brain=Brain()

#DEFINING CONTROLLERS AND MOTORS
Controller1 = Controller()
#NUMBER IN BRACKETS IS PORT
motor1 = Motor(1)
motor2 = Motor(2)
motor3 = Motor(3)
motor4 = Motor(4)

#ASSIGNING THE MOTORS TO THE CORRECT GROUPS
motorsLeft = MotorGroup(motor1, motor2)
motorsRight = MotorGroup(motor3, motor4)

#TESTING PRINT
Brain.screen.print("Program Loaded!")

#IS CALLED WHEN AXIS2 (RIGHT JOYSTICK - VERTICAL) IS CHANGED
def axisChanged2():
    #DEFINE POSITION OF CONTROLLER JOYSTICK
    pos = Controller1.axis1.position()
    #WHEN POS IS < 0 IT IS POINTING DOWN AND WE MOVE REVERSE
    if pos < 0:
        motorsRight.spin(REVERSE)
        motorsRight.set_velocity(pos, PERCENT)
    else:
        motorsRight.spin(FORWARD)
        motorsRight.set_velocity(pos, PERCENT)

#IS CALLED WHEN AXIS3 (LEFT JOYSTICK - VERTICAL) IS CHANGED
def axisChanged3():
    pos = Controller1.axis3.position()
    
    if pos < 0:
        motorsLeft.spin(REVERSE)
        motorsLeft.set_velocity(pos, PERCENT)
    else:
        motorsRight.spin(FORWARD)
        motorsLeft.set_velocity(pos, PERCENT)

#LISTENS FOR A CHANGE IN JOYSTICKS
Controller1.axis2.changed(axisChanged2)
Controller1.axis3.changed(axisChanged3)