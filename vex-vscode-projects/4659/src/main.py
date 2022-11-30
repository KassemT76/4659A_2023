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
import sys

#Config----------------------------------------------------#
brain          = Brain()
Controller1    = Controller()

Flywheel1      = Motor(Ports.PORT11, GearSetting.RATIO_6_1  , True  )    #Do not change gear ratio
Flywheel2      = Motor(Ports.PORT12, GearSetting.RATIO_6_1  , False )    #Do not change gear ratio
Intake         = Motor(Ports.PORT13, GearSetting.RATIO_36_1 , True  )    #Not Finalized  
Rollers        = Motor(Ports.PORT21, GearSetting.RATIO_18_1 , False )    #Not Finalized
LFMotor        = Motor(Ports.PORT11, GearSetting.RATIO_36_1 , True )
LRMotor        = Motor(Ports.PORT12, GearSetting.RATIO_36_1 , True )
RFMotor        = Motor(Ports.PORT13, GearSetting.RATIO_36_1 , False  )
RRMotor        = Motor(Ports.PORT14, GearSetting.RATIO_36_1 , False )

p1 = Pneumatics(brain.three_wire_port.h)

opticSens = Optical(Ports.PORT1)

encL = Encoder(brain.three_wire_port.c)
encL2 = Encoder(brain.three_wire_port.d)
encR = Encoder(brain.three_wire_port.a)
encR2 = Encoder(brain.three_wire_port.b)

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


RHDrive  = MotorGroup(RFMotor, RRMotor)
LHDrive  = MotorGroup(LFMotor, LRMotor)
Flywheel = MotorGroup(Flywheel1, Flywheel2)

#First print
brain.screen.print("Program Loaded!")
#Information header
brain.screen.clear_line()
brain.screen.set_cursor(1,0)
brain.screen.print("Information: ")

# Calibration ---------------------------------------------------#

encL.reset_position()
encL2.reset_position()
encR.reset_position()
encR2.reset_position()

#Low Level Services----------------------------------------------#

#Find distance travelled from encoder
def findDistance(encoder):
    Encoder.value

#Figure out actual flywheel rpm
def flywheelRPM():
    GavinWasHere = Flywheel.velocity(VelocityUnits.RPM) * 6
    return(GavinWasHere)

#Threading-------------------------------------------------------#
def intakeControl():  #This is a intake control thread
    while True:
        if intakeStatus == True:
            Intake.set_velocity(100, PERCENT)

        else: 
            Intake.set_velocity(0  , PERCENT)

def flywheelControl(RPM):
    global startUp
    if startUp == False:      #Turn on flywheel
        Flywheel.set_velocity((Flywheel.velocity(VelocityUnits.RPM)), VelocityUnits.RPM)
        internalRPM = Flywheel.velocity(VelocityUnits.RPM)
        while internalRPM <= startUpRPM:
            Flywheel.set_velocity(internalRPM, VelocityUnits.RPM)
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
ppos = 1
ppos2 = 1
ppos3 = 1
ppos4 =1
#IS CALLED WHEN AXIS2 (RIGHT JOYSTICK - VERTICAL) IS CHANGED
def moveMRight():
    global ppos
    global ppos2
    #DEFINE POSITION OF CONTROLLER JOYSTICK
    pos = Controller1.axis2.position()
    #WHEN POS IS < 0 IT IS POINTING DOWN AND WE MOVE REVERSE
    if pos < 0:
        RHDrive.spin(REVERSE)
        if pos < ppos:
            RHDrive.set_velocity((pos/4)*setSpeed, PERCENT)
        ppos = int(pos/10+0.99)*10
    elif pos > 0:
        RHDrive.spin(FORWARD)
        if pos > ppos2:
            RHDrive.set_velocity((pos/4)*setSpeed, PERCENT)
        ppos2 = int(pos/10+0.99)*10
    else:
        RHDrive.set_velocity(0, PERCENT)
    #PRINTS INFO
    brain.screen.set_cursor(4,0)
    brain.screen.clear_row()
    brain.screen.print("Axis 2: ", Controller1.axis2.position())
   

#IS CALLED WHEN AXIS3 (LEFT JOYSTICK - VERTICAL) IS CHANGED
def moveMLeft():
    global ppos3
    global ppos4
    #DEFINE POSITION OF CONTROLLER JOYSTICK
    pos1 = Controller1.axis3.position()
    #WHEN POS IS < 0 IT IS POINTING DOWN AND WE MOVE REVERSE
    if pos1 < 0:
        LHDrive.spin(REVERSE)
        if pos1 < ppos3:
            LHDrive.set_velocity((pos1/4)*setSpeed, PERCENT)
        
    elif pos1 > 0:
        LHDrive.spin(FORWARD)
        if pos1 > ppos4:
            LHDrive.set_velocity((pos1/4)*setSpeed, PERCENT)
    else:
        LHDrive.set_velocity(0, PERCENT)
    ppos3 = int(pos1/10+0.99)*10
    ppos4 = int(pos1/10+0.99)*10
    #PRINTS INFO
    brain.screen.set_cursor(3,0)
    brain.screen.clear_row()
    brain.screen.print("Axis 3: ", Controller1.axis3.position())

def odometry():
    posx = 0
    posy = 0
    
    distance_per_rotation = 25.93 # Measurement in CENTIMETERS
    while True:
        brain.screen.set_cursor(8,0)
        brain.screen.clear_line()
        brain.screen.print("Left Encoder: ", encL.value()/360 * distance_per_rotation)
        brain.screen.set_cursor(9,0)
        brain.screen.clear_line()
        brain.screen.print("Right Encoder: ", encR.value()/360 * distance_per_rotation)
        wait(500)

def roller():
    x = opticSens.color()    
    brain.screen.print(x)
    if x == Color.RED:
        brain.screen.print("ajsjds")
#Competition Templating----------------------------------------------------------------------------------#

def driver():
    #LISTENS FOR A CHANGE IN JOYSTICKS
    Controller1.axis2.changed(moveMRight)
    Controller1.axis3.changed(moveMLeft)
    #ARROW BUTTONS TO CHANGE SPEED
    Controller1.buttonDown.pressed(changeSpeedDown)
    Controller1.buttonUp.pressed(changeSpeedUp)  
    Controller1.buttonRight.pressed(changeSpeedN)
    #BUTTON TO TEST AUTONUM IN DRIVE MODE
    Controller1.buttonB.pressed(roller)
    odometry()

def autonum():
    odometry()
                
#INITIALIZING COMPETITION MODE
comp = Competition(driver, autonum)