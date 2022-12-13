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

Flywheel      = Motor(Ports.PORT7, GearSetting.RATIO_6_1  , True  )    #Do not change gear ratio

Intake         = Motor(Ports.PORT6, GearSetting.RATIO_36_1 , True  )    

LFMotor        = Motor(Ports.PORT1, GearSetting.RATIO_36_1 , True )
LRMotor        = Motor(Ports.PORT2, GearSetting.RATIO_36_1 , True )
RFMotor        = Motor(Ports.PORT3, GearSetting.RATIO_36_1 , False  )
RRMotor        = Motor(Ports.PORT4, GearSetting.RATIO_36_1 , False )

SIG_1 = Signature(1, 6035, 7111, 6572, -1345, -475, -910, 3.000, 0)
opticSens = Optical(Ports.PORT11)
visionSens = Vision(Ports.PORT9, 50, SIG_1)

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
opp_team = Color.BLUE # 
position = [0.0, 0.0]
oldPos = 0

#Motor Grouping---------------------------------------------------#
RHDrive  = MotorGroup(RFMotor, RRMotor)
LHDrive  = MotorGroup(LFMotor, LRMotor)

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
def findDistanceY(distance, angle):
    global oldPos 
    newPos = distance - oldPos

    distance += newPos*math.sin(angle)

    return distance


def findDistanceX(distance, angle):
    global oldPos 
    newPos = distance - oldPos

    distance += newPos*math.cos(angle)

    return distance


def odometry():
    global position
    
    # FIND DISTANCE TRAVELLED
    distance_per_rotation = 10.21 # Measurement in INCHES

    d_left = encL.value()/360 * distance_per_rotation
    d_right = encR.value()/360 * distance_per_rotation
    d_average = (d_left + d_right) / 2

    #CALCULATE ORIENTATION
    back_tracking_distance = 9.81 # INCHES
    horizontal_tracking_distance = 3.535 # INCHES
    angle = (d_left - d_right) / (2 * horizontal_tracking_distance) # RADIANS

    #COORDINATES
    position[0] = findDistanceX(d_average, angle)
    position[1] = findDistanceY(d_average, angle)

    #math.sin(angle * 180 / math.pi)

    # PRINT ENCODER VALUES
    brain.screen.set_cursor(2,0)
    brain.screen.clear_line()
    brain.screen.print("Left Encoder: ", d_left)

    brain.screen.set_cursor(3,0)
    brain.screen.clear_line()
    brain.screen.print("Right Encoder: ", d_right)

    brain.screen.set_cursor(4,0)
    brain.screen.clear_line()
    brain.screen.print("Middle Encoder: ", encM.value(), encM.value()/360 * distance_per_rotation)
    
    brain.screen.set_cursor(5,0)
    brain.screen.clear_line()
    brain.screen.print("Position: ", "X", position[0], "Y", position[1])

    brain.screen.set_cursor(6,0)
    brain.screen.clear_line()
    brain.screen.print("Orientation: ", (angle * 180 / math.pi))

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
    brain.screen.set_cursor(7,0)
    brain.screen.clear_row()

    brain.screen.print("Axis 2: ", Controller1.axis2.position())
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
    brain.screen.set_cursor(8,0)
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
#   -Vision sensors
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def roller():
    global team
    opticColor = opticSens.color() 

    if opticColor == opp_team:
        Intake.spin(FORWARD, 100, RPM)   

    brain.screen.set_cursor(9,0)
    brain.screen.clear_line()
    brain.screen.print("Color ", opticColor)

    if opticColor == team:
        Intake.stop()

    wait(50)

def locator():
    x = visionSens.take_snapshot(SIG_1)
    if x != None:
        brain.screen.set_cursor(10,0)
        brain.screen.clear_line()
        print(x[0].centerX)
        if x[0].centerX < 130:
            LHDrive.spin(REVERSE, 10)
            RHDrive.spin(FORWARD, 10)
            
        elif x[0].centerX > 170:
            LHDrive.spin(FORWARD, 10)
            RHDrive.spin(REVERSE, 10)

        else:
            LHDrive.stop()
            RHDrive.stop()

        
        
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
        roller()
        wait(15) 

def autonum():
    while True:
        odometry()
        locator()


        wait(50)
            
#INITIALIZING COMPETITION MODE
comp = Competition(driver, autonum)
