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
import math 

# CONFIGURATION ------------------------------------------------------------------#
#
#   INCLUDES
#
#   -Variable Definitions
#   -Calibration
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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
encM = Encoder(brain.three_wire_port.e)
encM2 = Encoder(brain.three_wire_port.f)

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

#Changable globals
team = Color.RED # Color.RED for RED, Color.BlUE for BLUE
position = [0.0, 0.0]
orientation = 90 # Value in degrees (90 = facing forwards)

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

def pre_autonum():  
    encL.reset_position()
    encL2.reset_position()
    encR.reset_position()
    encR2.reset_position()

# Low Level Services ------------------------------------------------------------------#
#
#   INCLUDES
#
#   -Odometry
#   -PID controls
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#Find distance travelled from encoder
def odometry():
    global position
    global orientation
    
    distance_per_rotation = 10.21 # Measurement in INCHES

    d_left = encL.value()/360 * distance_per_rotation
    d_right = encR.value()/360 * distance_per_rotation
    d_average = (d_left + d_right) / 2

    position[0] = math.cos(orientation) * d_average
    position[1] = math.sin(orientation) * d_average

    # PRINT ENCODER VALUES
    brain.screen.set_cursor(8,0)
    brain.screen.clear_line()
    brain.screen.print("Left Encoder: ", d_left)


    brain.screen.set_cursor(9,0)
    brain.screen.clear_line()
    brain.screen.print("Right Encoder: ", d_right)

    brain.screen.set_cursor(10,0)
    brain.screen.clear_line()
    brain.screen.print("Middle Encoder: ", encM.value(), encM.value()/360 * distance_per_rotation)
    
    brain.screen.set_cursor(11,0)
    brain.screen.clear_line()
    brain.screen.print("Y-Position: ", position[1])
    wait(15)

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

# #Driving Controls------------------------------------------------------------------#
#
#   INCLUDES
#
#   -SPEED CONTROLS
#   -MOTOR MOVEMENT
#   -TEST FUNCTION
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
        RHDrive.spin(REVERSE)
        RHDrive.set_velocity((pos/4)*setSpeed, PERCENT)
    #PRINTS INFO
    brain.screen.set_cursor(4,0)
    brain.screen.clear_row()

    brain.screen.print("Axis 2: ", Controller1.axis2.position())
    brain.screen.print("Axis 2: ", Controller1.axis2.position(), "Velocity: ", RHDrive.velocity() )

   

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

def testFunction():
    LHDrive.spin_for(FORWARD, 360, DEGREES, 10, RPM, wait=False)
    RHDrive.spin_for(REVERSE, 360, DEGREES, 10, RPM)

# #Autonum Controls------------------------------------------------------------------#
#
#   INCLUDES
#
#   -ROLLER MOVEMENT
# 
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def roller():
    global team
    x = 0

    Rollers.spin(FORWARD, 100, RPM)
    while x != 1:
        opticColor = opticSens.color() 
        brain.screen.set_cursor(12,0)
        brain.screen.clear_line()
        brain.screen.print("Color ", opticColor)
        if opticColor == team:
            Rollers.stop()
            x=1 
        wait(50)
        
# Competition Templates Controls------------------------------------------------------------------#
#
#   INCLUDES
#
#   -DRIVER TEMPLATE
#   -AUTONUM TEMPLATE
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

pre_autonum()

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
    #turn on odometry
    while True:
        odometry()
        wait(15) 

def autonum():
    while True:
        odometry()
        if position[1] < 10:
            LHDrive.spin(FORWARD, 10, RPM)
            RHDrive.spin(FORWARD, 10, RPM)
        else:
            LHDrive.stop()
            RHDrive.stop()
#INITIALIZING COMPETITION MODE
comp = Competition(driver, autonum)
