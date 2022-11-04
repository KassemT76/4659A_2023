# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       super                                                        #
# 	Created:      2022-10-19                                                   #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
import vex 
import sys

#Config----------------------------------------------------#
brain          = vex.Brain()
Controller1    = vex.Controller()

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
setSpeed = 2

#Motor Grouping---------------------------------------------------#
LHDrive  = vex.MotorGroup(LFMotor, LRMotor)
RHDrive  = vex.MotorGroup(RFMotor, RRMotor)
Flywheel = vex.MotorGroup(Flywheel1, Flywheel2)

#First print
brain.screen.print("Program Loaded!")
#Information header
brain.screen.clear_line()
brain.screen.set_cursor(1,0)
brain.screen.print("Information: ")

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

#Driving Controls------------------------------------------------------------------#

#Speed Settings-------------------------------------------#
def changeSpeedDown():
    global setSpeed
    setSpeed = 2
    Controller1.screen.clear_row(1)
    Controller1.screen.set_cursor(1,0)
    Controller1.screen.print("Speed",setSpeed)

def changeSpeedN():
    global setSpeed
    setSpeed = 3
    Controller1.screen.clear_row(1)
    Controller1.screen.print("Speed",setSpeed)
    
def changeSpeedUp():
    global setSpeed
    setSpeed = 4
    Controller1.screen.clear_row(1)
    Controller1.screen.print("Speed",setSpeed)

#Moving the motors----------------------------------------#

#IS CALLED WHEN AXIS2 (RIGHT JOYSTICK - VERTICAL) IS CHANGED
def moveMRight():
    #DEFINE POSITION OF CONTROLLER JOYSTICK
    pos = Controller1.axis2.position()
    #WHEN POS IS < 0 IT IS POINTING DOWN AND WE MOVE REVERSE
    if pos < 0:
        RHDrive.spin(vex.REVERSE)
        RHDrive.set_velocity((pos/4)*setSpeed, vex.PERCENT)
    else:
        RHDrive.spin(vex.FORWARD)
        RHDrive.set_velocity((pos/4)*setSpeed, vex.PERCENT)
    #PRINTS INFO
    brain.screen.set_cursor(2,0)
    brain.screen.clear_row()
    brain.screen.print("Axis 2: ", Controller1.axis2.position(), "Velocity: ", RHDrive.velocity() )
   

#IS CALLED WHEN AXIS3 (LEFT JOYSTICK - VERTICAL) IS CHANGED
def moveMLeft():
    global setSpeed
    #DEFINE POSITION OF CONTROLLER JOYSTICK
    pos1 = Controller1.axis3.position()
    #WHEN POS IS < 0 IT IS POINTING DOWN AND WE MOVE REVERSE
    if (pos1 < 0):
        LHDrive.spin(vex.REVERSE)
        #if pos1%4 == 0
        LHDrive.set_velocity((pos1/4)*setSpeed, vex.PERCENT)
    elif (pos1 >= 0):
        LHDrive.spin(vex.FORWARD)
        LHDrive.set_velocity((pos1/4)*setSpeed, vex.PERCENT)

    #PRINTS INFO
    brain.screen.set_cursor(3,0)
    brain.screen.clear_row()
    brain.screen.print("Axis 3 Changed: ", Controller1.axis3.position(),"Velocity: ", LHDrive.velocity())


#Competition Templating----------------------------------------------------------------------------------#

def driver():
    #LISTENS FOR A CHANGE IN JOYSTICKS
    Controller1.axis2.changed(moveMRight)
    Controller1.axis3.changed(moveMLeft)
    #BUTTON TO TEST AUTONUM IN DRIVE MODE
    Controller1.buttonA.pressed(autonum)
    #ARROW BUTTONS TO CHANGE SPEED
    Controller1.buttonDown.pressed(changeSpeedDown)
    Controller1.buttonUp.pressed(changeSpeedUp)  
    Controller1.buttonRight.pressed(changeSpeedN)
    vex.wait(5)

def autonum():
         LHDrive.spin_for(vex.FORWARD, 360, vex.DEGREES, 300, vex.RPM, wait = False)
         RHDrive.spin_for(vex.FORWARD, 360, vex.DEGREES, 300, vex.RPM, wait = False)

#INITIALIZING COMPETITION MODE
comp = vex.Competition(driver, autonum)


    
