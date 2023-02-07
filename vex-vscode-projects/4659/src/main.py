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

Flywheel      = Motor(Ports.PORT9, GearSetting.RATIO_6_1  , False  )    #Do not change gear ratio

Intake         = Motor(Ports.PORT8, GearSetting.RATIO_36_1 , True  )    

LFFMotor       = Motor(Ports.PORT5, GearSetting.RATIO_36_1 , False )
LFMotor        = Motor(Ports.PORT1, GearSetting.RATIO_36_1 , True )
LRMotor        = Motor(Ports.PORT2, GearSetting.RATIO_36_1 , True )

RFFMotor       = Motor(Ports.PORT6, GearSetting.RATIO_36_1 , True )
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

clutchPiston = Pneumatics(brain.three_wire_port.g)

#Program Internal Constants--------(Don't screw arround with this if you don't know what you are doing.)-----------#
intakeStatus = False   #Switch for turning on and off intake. Set this variable to False in your code if u wanna switch it off.
flywheelTargetRpm  = 3600       #The only thing that should touch this variable, is the flywheel control program, and the physics equation

#DO NOT TOUCH U CAN DESTROY HARDWARE If you think this is an issue ask Gavin before changing stuff. (Gavin's Notes: Used for controlling startup and shutdown of flywheel)
startUp      = False #False is flywheel startup not complete, True is complete
Shutdown     = False #Used for shutting down flywheel
startUpRPM   = 200
internalRPM  = 0
RPMIncrement = 10
setSpeed = 2
RPMDelay     = 0.025

#Changable globals
team = Color.RED # Color.RED for RED, Color.BlUE for BLUE
opp_team = Color.BLUE # 
position = [0.0, 0.0]
#Odometry
old_left = 0
old_right = 0
angle = 0
#Intake
intakeSpeed = 200
#Flywheel
clutchActivate = False
#START ON ROLLER FOR AUTONOMOUS
start_on_roller = False

#Motor Grouping---------------------------------------------------#
RHDrive  = MotorGroup(RFFMotor, RFMotor, RRMotor)
LHDrive  = MotorGroup(LFFMotor, LFMotor, LRMotor)

#First print
brain.screen.print("Program Loaded!")
#Information header
brain.screen.clear_line()
brain.screen.set_cursor(1,0)
brain.screen.print("Information: ")

def initialization():  
    encL.reset_position()
    encL2.reset_position()
    encR.reset_position()
    encR2.reset_position()

def driver_initialization():
    global startUp
    global intakeStatus
    
    initialization()

    startUp = False
    flywheelStartup()

    intakeStatus = True
    intakeControl()
    
    
def auton_inititialization():
    global startUp
    global intakeStatus
    
    initialization()

    startUp = False
    flywheelStartup()

    intakeStatus = True
    intakeControl()


def shutDown():
    LHDrive.stop()
    RHDrive.stop()
    Intake.stop()
    flywheelShutdown()

# Low Level Services ------------------------------------------------------------------#
#
#   INCLUDES
#
#   -Odometry
#   -PID controls
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#Find distance travelled
def odometry():
    global position, angle, old_left, old_right
    
    # FIND DISTANCE TRAVELLED
    distance_per_rotation = 10.21 # Measurement in INCHES
    back_tracking_distance = 9.81 # INCHES
    horizontal_tracking_distance = 3.535 # INCHES

    new_left = encL.value() 
    new_right = encR.value() 

    d_left = ((new_left - old_left) * distance_per_rotation)/360
    d_right = ((new_right - old_right) * distance_per_rotation)/360

    
    #CALCULATE ORIENTATION
    d_angle = (d_left - d_right) / (2 * horizontal_tracking_distance) # RADIANS


    # if angle > math.pi/2 - 0.1 and angle < math.pi/2 + 0.1:
    #     angle = math.pi/2
    # elif angle > math.pi - 0.1 and angle < math.pi + 0.1:
    #     angle = math.pi
    # elif angle > math.pi*2 - 0.1 and angle < math.pi*2 + 0.1:
    #     angle = math.pi*2
    # elif angle > -0.1 and angle < 0.1:
    #     angle = 0

    if d_angle == 0:
        position[0] += d_left * math.sin(angle)
        position[0] += d_left * math.cos(angle)
    else:
        side_arc  = 2 * ((d_left/ d_angle) + horizontal_tracking_distance) * math.sin(d_angle / 2)
        DeltaYSide = side_arc * math.cos(angle + (d_angle / 2))
        DeltaXSide = side_arc * math.sin(angle + (d_angle / 2))
        angle += d_angle
        position[0] += DeltaXSide
        position[1] += DeltaYSide

    old_left = new_left
    old_right = new_right
    d_angle = 0

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
    brain.screen.print("Orientation: ", angle)

#Threading-------------------------------------------------------#
def intakeControl():  #This is a intake control thread
    global intakeStatus, intakeSpeed

    if intakeStatus == True:
        Intake.spin(FORWARD, intakeSpeed, RPM)
    else:
        Intake.stop()


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

ppos  = 1
ppos2 = 1
ppos3 = 1
ppos4 = 1

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
    brain.screen.print("Axis 2: ",
     Controller1.axis2.position())

   

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
def intakeButton():
    global intakeStatus

    intakeStatus = not(intakeStatus)
    intakeControl()

def flywheelShoot():
    global clutchActivate, intakeSpeed

    clutchActivate = not(clutchActivate)
    
    if clutchActivate == True:
        clutchPiston.open()
        Intake.spin(REVERSE, 40, RPM)
    else: 
        clutchPiston.close()
        Intake.spin(FORWARD, intakeSpeed, RPM)
    
def roller():
    global team, intakeSpeed
    opticColor = opticSens.color() 

    if opticColor == opp_team:
        Intake.spin(FORWARD, intakeSpeed, RPM)   

    brain.screen.set_cursor(9,0)
    brain.screen.clear_line()
    brain.screen.print("Color ", opticColor)

    if opticColor == team:
        # CHANGE TO NOT INTERFERE WITH INDEXER
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

initialization()

#Competition Templating----------------------------------------------------------------------------------#
def driver():
    driver_initialization()
    #LISTENS FOR A CHANGE IN JOYSTICKS
    Controller1.axis2.changed(moveMRight)
    Controller1.axis3.changed(moveMLeft)
    #ARROW BUTTONS TO CHANGE SPEED
    Controller1.buttonDown.pressed(changeSpeedDown)
    Controller1.buttonUp.pressed(changeSpeedUp)  
    Controller1.buttonRight.pressed(changeSpeedN)
    #BUTTON TO TEST AUTONUM IN DRIVE MODE
    Controller1.buttonB.pressed(roller)
    Controller1.buttonL1.pressed(intakeButton)
    Controller1.buttonR1.pressed(flywheelStartup)
    Controller1.buttonR2.pressed(flywheelShoot)
    Controller1.buttonL2.pressed(flywheelShutdown)

    # #turn on odometry
    # while True:
    #     odometry()
    #     wait(500)


def roller_start():
    # Perform Roller Job
    LHDrive.spin_for(REVERSE, 90)
    RHDrive.spin_for(REVERSE, 90)
    roller()
    LHDrive.spin_for(FORWARD, 90)
    RHDrive.spin_for(FORWARD, 90)
    Intake.spin(FORWARD, intakeSpeed, RPM)


    # Move to disks
    while(True):
        odometry()
        LHDrive.spin(REVERSE, 15, RPM)
        RHDrive.spin(FORWARD, 15, RPM)
        if angle >= 2.36:
            break

    LHDrive.spin_for(FORWARD, 1080)
    RHDrive.spin_for(FORWARD, 1080)


    # Turn and shoot
    while(True):
        odometry()
        LHDrive.spin(REVERSE, 15, RPM)
        RHDrive.spin(FORWARD, 15, RPM)
        if angle >= 3.93:
            break
    

    flywheelShoot()
    wait(200)
    flywheelShoot()
    
def regular_start():
    pass


def autonum():
    global start_on_roller

    auton_inititialization()

    if start_on_roller:
        roller_start()
    else:
        regular_start()

comp = Competition(driver, autonum)
