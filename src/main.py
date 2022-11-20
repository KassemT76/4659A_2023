# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       gavin                                                        #
# 	Created:      2022-10-20, 12:23:57 p.m.                                    #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library Imports
from vex import *
import sys

#Config----------------------------------------------------#
brain          = Brain()

Flywheel       = Motor(Ports.PORT11, GearSetting.RATIO_6_1  , True  )    #Do not change gear ratio
LFMotor        = Motor(Ports.PORT15, GearSetting.RATIO_36_1 , False )
LRMotor        = Motor(Ports.PORT18, GearSetting.RATIO_36_1 , False )
RFMotor        = Motor(Ports.PORT19, GearSetting.RATIO_36_1 , True  )
RRMotor        = Motor(Ports.PORT20, GearSetting.RATIO_36_1 , False )


#Program Internal Constants--------(Don't screw arround with this if you don't know what you are doing.)-----------#
flywheelTargetRpm  = 3600       #The only thing that should touch this variable, is the flywheel control program, and the physics equation

#DO NOT TOUCH U CAN DESTROY HARDWARE If you think there is an issue ask Gavin before changing stuff. (Gavin's Notes: Used for controlling startup and shutdown of flywheel)
startUp      = False #False is flywheel startup not complete, True is complete
Shutdown     = False #Used for shutting down flywheel
startUpRPM   = 580
internalRPM  = 0
RPMIncrement = 1                            #tune for startup/shutdown speed
RPMDelay     = 0.025   #delay in seconds          tune for startup/shutdown speed

#Motor Grouping---------------------------------------------------#
LHDrive  = MotorGroup(LFMotor, LRMotor)
RHDrive  = MotorGroup(RFMotor, RRMotor)

#Low Level Services----------------------------------------------#

#Figure out actual flywheel rpm
def flywheelRPM():
    Kassemsayshewantsavariableinthiscodenamedafterhim = Flywheel.velocity(VelocityUnits.RPM) * 6
    return(Kassemsayshewantsavariableinthiscodenamedafterhim)

def flywheelStartup():
    Flywheel.spin(FORWARD, Flywheel.velocity(VelocityUnits.RPM), VelocityUnits.RPM)
    internalRPM = Flywheel.velocity(VelocityUnits.RPM)
    while internalRPM <= startUpRPM:
        Flywheel.spin(FORWARD, internalRPM, VelocityUnits.RPM)
        internalRPM = internalRPM + RPMIncrement
        wait(RPMDelay, SECONDS)
    startUp = True

def flywheelShutdown():
    internalRPM = Flywheel.velocity(VelocityUnits.RPM)
    while internalRPM > 0:
        Flywheel.spin(FORWARD, internalRPM, VelocityUnits.RPM)
        internalRPM = internalRPM - RPMIncrement
        wait(RPMDelay, SECONDS)
    Flywheel.spin(FORWARD, 0, VelocityUnits.RPM)


#Threading-------------------------------------------------------#

def flywheelControl(RPM):
    if startUp == True and Shutdown == False:
        print("Pid goes here")






#test procedure

flywheelStartup()
print('lol')
wait(5, SECONDS)
flywheelShutdown()


