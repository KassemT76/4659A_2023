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

#IS CALLED WHEN AXIS2 IS CHANGED
def axisChanged2():
    #DEFINE POSITION OF CONTROLLER JOYSTICK
    pos = Controller1.axis1.position()
    #WHEN POS IS < 0 IT IS POINTING DOWN AND WE MOVE REVERSE
    if pos < 0:
        motorsLeft.spin(REVERSE)
    else:
        motorsLeft.spin(FORWARD)

#IS CALLED WHEN AXIS2 IS CHANGED
def axisChanged3():
    pos = Controller1.axis3.position()

#LISTENS FOR A CHANGE IN JOYSTICKS
Controller1.axis2.changed(axisChanged2)
Controller1.axis3.changed(axisChanged3)

#old code to convert to python

# void axis2(){
#   float pos = Controller1.Axis2.position(percent);
#   Brain.Screen.clearLine();
#   Brain.Screen.print("A2: ");
#   Brain.Screen.print(pos); 

#   if (pos < 0)
#   {
#     motorsRight.spin(reverse);
#     motorsRight.setVelocity(pos, percent);
#   }
#   else 
#   {
#     motorsRight.spin(forward);
#     motorsRight.setVelocity(pos, percent);
#   }
# }

# //up and down on left joy

# void axis3(){
#   float pos = Controller1.Axis3.position(percent);

#   if (pos < 0){
#     motorsLeft.spin(reverse);
#     // motorsRight.spin(reverse);
#     motorsLeft.setVelocity(pos, percent);
#     // motorsRight.setVelocity(pos, percent);
#   }
#   else {
#     motorsLeft.spin(forward);
#     // motorsRight.spin(forward);
#     motorsLeft.setVelocity(pos, percent);
#     // motorsRight.setVelocity(pos, percent);
#   }

#   Brain.Screen.clearLine();
#   Brain.Screen.print("A3: ");
#   Brain.Screen.print(pos); 
# }

        
