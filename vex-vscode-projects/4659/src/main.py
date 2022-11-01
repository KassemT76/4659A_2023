# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       super                                                        #
# 	Created:      2022-10-19                                                   #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

#DEFINING CONTROLLERS AND MOTORS
Controller1 = Controller()
#INITIALIZING MOTORS
motor1 = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)
motor2 = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)
motor3 = Motor(Ports.PORT7, GearSetting.RATIO_6_1, False)
motor4 = Motor(Ports.PORT8, GearSetting.RATIO_6_1, False)

#ASSIGNING THE MOTORS TO THE CORRECT GROUPS
motorsLeft = MotorGroup(motor1, motor2)
motorsRight = MotorGroup(motor3, motor4)

#TESTING PRINT
brain.screen.print("Program Loaded!")

#IS CALLED WHEN AXIS2 (RIGHT JOYSTICK - VERTICAL) IS CHANGED
def moveMRight():
    #DEFINE POSITION OF CONTROLLER JOYSTICK
    pos = Controller1.axis2.position()
    #WHEN POS IS < 0 IT IS POINTING DOWN AND WE MOVE REVERSE
    if pos < 0:
        motorsRight.spin(REVERSE)
        if (pos%4)==0:
            motorsRight.set_velocity(pos, PERCENT)
    else:
        motorsRight.spin(FORWARD)
        if (pos%4)==0:
            motorsRight.set_velocity(pos, PERCENT)

#IS CALLED WHEN AXIS3 (LEFT JOYSTICK - VERTICAL) IS CHANGED
def moveMLeft():
    #DEFINE POSITION OF CONTROLLER JOYSTICK
    pos1 = Controller1.axis3.position()
    #WHEN POS IS < 0 IT IS POINTING DOWN AND WE MOVE REVERSE
    if pos1 < 0:
        motorsLeft.spin(REVERSE)
        if (pos1 % 4) == 0:
            motorsLeft.set_velocity(pos1, PERCENT)
    else:
        motorsLeft.spin(FORWARD)
        if (pos1 % 4) == 0:
            motorsLeft.set_velocity(pos1, PERCENT)

def driver():
    #LISTENS FOR A CHANGE IN JOYSTICKS
    Controller1.axis2.changed(moveMRight)
    Controller1.axis3.changed(moveMLeft)
    #BUTTON TO TEST AUTONUM IN DRIVE MODE
    Controller1.buttonA.pressed(autonum)

def autonum():
         motorsLeft.spin_for(REVERSE, 360, DEGREES, 300, RPM, wait = False)
         motorsRight.spin_for(FORWARD, 360, DEGREES, 300, RPM, wait = False)

#INITIALIZING COMPETITION MODE
comp = Competition(driver, autonum)
