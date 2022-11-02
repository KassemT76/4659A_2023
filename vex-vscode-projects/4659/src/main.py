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
Thread.sleep_for(1000, MSEC)
#INFORMATION HEADER
brain.screen.clear_line()
brain.screen.set_cursor(1,0)
brain.screen.print("Information: ")

setSpeed = 2


def changeSpeedDown():
    global setSpeed
    if setSpeed > 1:
        setSpeed -= 0.5
        Controller1.screen.clear_row(1)
        Controller1.screen.set_cursor(1,0)
        Controller1.screen.print("Speed",setSpeed)

def changeSpeedUp():
    global setSpeed
    if setSpeed < 4:
        setSpeed += 0.5
        Controller1.screen.clear_row(1)
        Controller1.screen.print("Speed",setSpeed)


#IS CALLED WHEN AXIS2 (RIGHT JOYSTICK - VERTICAL) IS CHANGED
def moveMRight():
    #DEFINE POSITION OF CONTROLLER JOYSTICK
    pos = Controller1.axis2.position()
    #WHEN POS IS < 0 IT IS POINTING DOWN AND WE MOVE REVERSE
    if pos < 0:
        motorsRight.spin(REVERSE)
        motorsRight.set_velocity((pos/4)*setSpeed, PERCENT)
    else:
        motorsRight.spin(FORWARD)
        motorsRight.set_velocity((pos/4)*setSpeed, PERCENT)
    #PRINTS INFO
    brain.screen.set_cursor(2,0)
    brain.screen.clear_row()
    brain.screen.print("Axis 2: ", Controller1.axis2.position(), "Velocity: ", motorsRight.velocity() )
    

#IS CALLED WHEN AXIS3 (LEFT JOYSTICK - VERTICAL) IS CHANGED
def moveMLeft():
    global setSpeed
    #DEFINE POSITION OF CONTROLLER JOYSTICK
    pos1 = Controller1.axis3.position()
    #WHEN POS IS < 0 IT IS POINTING DOWN AND WE MOVE REVERSE
    if (pos1 < 0):
        motorsLeft.spin(REVERSE)
        #if pos1%4 == 0
        motorsLeft.set_velocity(pos1/setSpeed, PERCENT)
    elif (pos1 >= 0):
        motorsLeft.spin(FORWARD)
        motorsLeft.set_velocity(pos1/setSpeed, PERCENT)

    #PRINTS INFO
    brain.screen.set_cursor(3,0)
    brain.screen.clear_row()
    brain.screen.print("Axis 3 Changed: ", Controller1.axis3.position(),"Velocity: ", motorsLeft.velocity())

def driver():
    #LISTENS FOR A CHANGE IN JOYSTICKS
    Controller1.axis2.changed(moveMRight)
    Controller1.axis3.changed(moveMLeft)
    #BUTTON TO TEST AUTONUM IN DRIVE MODE
    Controller1.buttonA.pressed(autonum)
    Controller1.buttonDown.pressed(changeSpeedDown)
    Controller1.buttonUp.pressed(changeSpeedUp)  # type: ignore
    wait(5, MSEC)


def autonum():
         motorsLeft.spin_for(FORWARD, 360, DEGREES, 300, RPM, wait = False)
         motorsRight.spin_for(FORWARD, 360, DEGREES, 300, RPM, wait = False)

#INITIALIZING COMPETITION MODE
comp = Competition(driver, autonum)


    
