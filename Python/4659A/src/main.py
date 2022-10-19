# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       super                                                        #
# 	Created:      2022-10-19, 3:46:18 p.m.                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from audioop import reverse
import struct
from turtle import forward
from vex import *

# Brain should be defined by default
Brain=Brain()
Controller1 = Controller()
motor1 = Motor(1)
motor2 = Motor(2)
motor3 = Motor(3)
motor4 = Motor(4)

motorsLeft = MotorGroup(motor1, motor2)
motorsRight = MotorGroup(motor3, motor4)

Brain.screen.print("Hello V5")

def axisChanged2():
    pos = Controller1.axis1.position()
    if pos < 0:
        motorsLeft.spin(reverse)
        motorsLeft.set_velocity(pos)
    else:
        motorsLeft.spin(forward)
    print(pos)

def axisChanged3():
    pos = Controller1.axis3.position()
    print(pos)

Controller1.axis2.changed(axisChanged2)
Controller1.axis3.changed(axisChanged3)

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

        
