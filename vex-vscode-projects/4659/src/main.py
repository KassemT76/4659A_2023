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
motor1 = Motor(Ports.PORT4, GearSetting.RATIO_6_1)
motor2 = Motor(Ports.PORT5, GearSetting.RATIO_6_1)
motor3 = Motor(Ports.PORT10, GearSetting.RATIO_6_1)
motor4 = Motor(Ports.PORT9, GearSetting.RATIO_6_1)

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
        #this should hopefully make the input less sensitive
        if pos % 4 == 0:
            motorsRight.set_velocity(pos, PERCENT)
    else:
        motorsRight.spin(FORWARD)
        #this should hopefully make the input less sensitive
        if pos % 4 == 0: 
            motorsRight.set_velocity(pos, PERCENT)

#IS CALLED WHEN AXIS3 (LEFT JOYSTICK - VERTICAL) IS CHANGED
def axisChanged3():
    #DEFINE POSITION OF CONTROLLER JOYSTICK
    pos1 = Controller1.axis3.position()
    #WHEN POS IS < 0 IT IS POINTING DOWN AND WE MOVE REVERSE
    if pos1 < 0:
        motorsLeft.spin(REVERSE)
        if pos1 % 4 == 0:
            motorsLeft.set_velocity(pos1, PERCENT)
        brain.screen.print("Moving reverse left")
    else:
        motorsLeft.spin(FORWARD)
        if pos1 % 4 == 0:
            motorsLeft.set_velocity(pos1, PERCENT)

def autonum():
         motorsLeft.spin_for(FORWARD, 1000, DEGREES, 100, RPM, wait = False)
         motorsRight.spin_for(FORWARD, 1000, DEGREES, 100, RPM, wait = False)

#LISTENS FOR A CHANGE IN JOYSTICKS
Controller1.axis2.changed(axisChanged2)
Controller1.axis3.changed(axisChanged3)
Controller1.buttonA.pressed(autonum)

#Joseph was here
