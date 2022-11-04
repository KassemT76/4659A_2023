# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       gavin                                                        #
# 	Created:      2022-10-20, 12:23:57 p.m.                                    #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library Imports
import vex
import sys
import numpy as np

#Config----------------------------------------------------#
brain          = vex.Brain()

Flywheel1      = vex.Motor(vex.Ports.PORT11, vex.GearSetting.RATIO_6_1  , True  )    #Do not change gear ratio
Flywheel2      = vex.Motor(vex.Ports.PORT12, vex.GearSetting.RATIO_6_1  , False )    #Do not change gear ratio
Intake         = vex.Motor(vex.Ports.PORT13, vex.GearSetting.RATIO_36_1 , True  )    #Not Finalized  
Rollers        = vex.Motor(vex.Ports.PORT21, vex.GearSetting.RATIO_18_1 , False )    #Not Finalized
LFMotor        = vex.Motor(vex.Ports.PORT15, vex.GearSetting.RATIO_36_1 , False )
LRMotor        = vex.Motor(vex.Ports.PORT18, vex.GearSetting.RATIO_36_1 , False )
RFMotor        = vex.Motor(vex.Ports.PORT19, vex.GearSetting.RATIO_36_1 , True  )
RRMotor        = vex.Motor(vex.Ports.PORT20, vex.GearSetting.RATIO_36_1 , False )


#Program Internal Constants--------(Don't screw arround with this if you don't know what you are doing.)-----------#
intakeStatus = False   #Switch for turning on and off intake. Set this variable to False in your code if u wanna switch it off.
flywheelTargetRpm  = 3600       #The only thing that should touch this variable, is the flywheel control program, and the physics equation

#DO NOT TOUCH U CAN DESTROY HARDWARE If you think this is an issue ask Gavin before changing stuff. (Gavin's Notes: Used for controlling startup and shutdown of flywheel)
startUp      = False #False is flywheel startup not complete, True is complete
Shutdown     = False #Used for shutting down flywheel
startUpRPM   = 580
internalRPM  = 0
RPMIncrement = 10

#Motor Grouping---------------------------------------------------#
LHDrive  = vex.MotorGroup(LFMotor, LRMotor)
RHDrive  = vex.MotorGroup(RFMotor, RRMotor)
Flywheel = vex.MotorGroup(Flywheel1, Flywheel2)

#Low Level Services----------------------------------------------#

#Figure out actual flywheel rpm
def flywheelRPM():
    GavinWasHere = Flywheel.velocity(vex.VelocityUnits.RPM) * 6
    return(GavinWasHere)

#Threading-------------------------------------------------------#
def intakeControl():  #This is a intake control thread
    while True:
        if intakeStatus == True:
            Intake.set_velocity(100, vex.PERCENT)

        else: 
            Intake.set_velocity(0  , vex.PERCENT)

def flywheelControl(RPM):
    if startUp == False:      #Turn on flywheel
        global startUp
        Flywheel.set_velocity((Flywheel.velocity(vex.VelocityUnits.RPM)), vex.VelocityUnits.RPM)
        internalRPM = Flywheel.velocity(vex.VelocityUnits.RPM)
        while internalRPM <= startUpRPM:
            Flywheel.set_velocity(internalRPM, vex.VelocityUnits.RPM)
            internalRPM = internalRPM + RPMIncrement
        startUp = True
            

    





    






def compStart():
   intakeControl()


