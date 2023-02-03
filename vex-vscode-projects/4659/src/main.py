# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Shome                                                        #
# 	Created:      2/1/2023, 1:42:57 PM                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
team = 1
from vex import *
import time
import math
brain=Brain()
Motor1 = Motor(Ports.PORT1,GearSetting.RATIO_36_1)
Motor2 = Motor(Ports.PORT1,GearSetting.RATIO_36_1)
Motor3 = Motor(Ports.PORT1,GearSetting.RATIO_36_1)
Motor4 = Motor(Ports.PORT1,GearSetting.RATIO_36_1)
Motor5 = Motor(Ports.PORT1,GearSetting.RATIO_36_1)
Motor6 = Motor(Ports.PORT1,GearSetting.RATIO_36_1)
Motor7 = Motor(Ports.PORT7,GearSetting.RATIO_18_1)
Encoder11 = Encoder(brain.three_wire_port.c)
Encoder12 = Encoder(brain.three_wire_port.d)
Encoder21 = Encoder(brain.three_wire_port.e)
Encoder22 = Encoder(brain.three_wire_port.f)
Encoder31 = Encoder(brain.three_wire_port.g)
Encoder32 = Encoder(brain.three_wire_port.h)
controller = Controller()
Encoder11.reset_position()
Encoder12.reset_position()
Encoder21.reset_position()
Encoder22.reset_position()
Encoder31.reset_position()
Encoder32.reset_position()

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)
class Manual:
    
    def __init__(self):
        self.NORMAL = (100/127)
        self.feather = [0.0, 0.0, 0.0, 0.0]

    def move(self):
        Motor1.spin(FORWARD, (controller.axis3.value()-controller.axis4.value()*self.NORMAL)*(2/3), PERCENT)
        Motor2.spin(FORWARD, (controller.axis3.value()-controller.axis4.value()*self.NORMAL)*(2/3), PERCENT)
        Motor3.spin(REVERSE, (controller.axis3.value()-controller.axis4.value()*self.NORMAL)*(2/3), PERCENT)
        Motor4.spin(REVERSE, (controller.axis3.value()-controller.axis4.value()*self.NORMAL)*(2/3), PERCENT)
        Motor5.spin(REVERSE, (controller.axis3.value()-controller.axis4.value()*self.NORMAL)*(2/3), PERCENT)
        Motor6.spin(FORWARD, (controller.axis3.value()-controller.axis4.value()*self.NORMAL)*(2/3), PERCENT)
    #1 is blue
    #2 is red
    def autoShoot(self,posX,posY,orientation,team):
        netposx=0
        netposy=0
        if (team == 1):
            netposx=980
            netposy=980
        elif (team == 2):
            netposx=20
            netposy=20
        if(controller.buttonLeft):

            distanceX = netposx-posX
            distanceY = netposy-posY
            force = (math.sqrt(distanceX+distanceY))*0.1
            desiredAngled = math.degrees(math.tan(distanceY/distanceX))
            angleDiff=desiredAngled-orientation
            start = time.time()
            end = start+2
            current = 0
            step = force / (2 * 100)
            while(abs(angleDiff) > 0.1):
                if(angleDiff > 0.1):
                    Motor1.spin(FORWARD, 100*self.NORMAL*(1/3), PERCENT)
                    Motor2.spin(FORWARD, 100*self.NORMAL*(1/3), PERCENT)
                    Motor3.spin(REVERSE, 100*self.NORMAL*(1/3), PERCENT)
                    Motor4.spin(FORWARD, 100*self.NORMAL*(1/3), PERCENT)
                    Motor5.spin(FORWARD, 100*self.NORMAL*(1/3), PERCENT)
                    Motor6.spin(REVERSE, 100*self.NORMAL*(1/3), PERCENT)
                elif (angleDiff < -0.1):
                    Motor1.spin(REVERSE, 100*self.NORMAL*(1/3), PERCENT)
                    Motor2.spin(REVERSE, 100*self.NORMAL*(1/3), PERCENT)
                    Motor3.spin(FORWARD, 100*self.NORMAL*(1/3), PERCENT)
                    Motor4.spin(REVERSE, 100*self.NORMAL*(1/3), PERCENT)
                    Motor5.spin(REVERSE, 100*self.NORMAL*(1/3), PERCENT)
                    Motor6.spin(FORWARD, 100*self.NORMAL*(1/3), PERCENT)
            while(time.time() < end):
                current += step
                time.sleep(0.01)
                Motor7.spin(FORWARD, force*self.NORMAL, PERCENT)
    
    def manShoot(self):
        speed = 0;
        if controller.buttonR2.pressing():
            speed = 85;
            self.feather[0] = 1;

        if controller.buttonR1.pressing():
            speed = 75;
            self.feather[0] = 1;

        if(speed > 0):
            Motor7.spin(REVERSE, self.NORMAL*(2/3), PERCENT)
        
        if(not controller.buttonR1.pressing() and not controller.buttonR2.pressing()):
            Motor7.set_velocity(self.feather[0])
            if(self.feather[0] >= 0):
                self.feather[0] -= 0.01
                wait(50, MSEC)

driver = Manual()
competitionVar = Competition
i=0
f=0
while True:
    print(Encoder11.value()," ", Encoder22.value()," ", Encoder21.value()," ", Encoder31.value())
    if(competitionVar.is_enabled() == True):
        if(competitionVar.is_driver_control()):
            driver.move()
            Motor7.spin(FORWARD,10,VoltageUnits.VOLT)
            #127
