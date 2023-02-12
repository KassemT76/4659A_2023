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
import time

# PREGAME CONFIG -----------------------------------------------------------------#
#
# INCLUDES
#
# - Team Colour
# - Robot Orientation
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

blue_team =  False
roller_orientation = False

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

RedSignature = Signature(1, 5763, 6739, 6250, -1257, -921, -1090, 8.900, 0)
BlueSignature  = Signature(1, 4347, 8243, 6294, -371, 1233, 432, 1.600, 0)


RedSignature = Signature(1, -3201, -2091, -2646, 7227, 13637, 10432, 2.400, 0)
BlueSignature  = Signature(1, -2299, -607, -1453, 2173, 5499, 3836, 1.700, 0)

opticSens = Optical(Ports.PORT11)
visionSens = Vision(Ports.PORT10, 150, BlueSignature, RedSignature)

pneumatic = Pneumatics(brain.three_wire_port.a)

encL = Encoder(brain.three_wire_port.c)
encL2 = Encoder(brain.three_wire_port.d)
encR = Encoder(brain.three_wire_port.a)
encR2 = Encoder(brain.three_wire_port.b)
encM = Encoder(brain.three_wire_port.e)
encM2 = Encoder(brain.three_wire_port.f)

#Program Internal Constants--------(Don't screw arround with this if you don't know what you are doing.)-----------#
intakeStatus = False   #Switch for turning on and off intake. Set this variable to False in your code if u wanna switch it off.
flywheelTargetRpm  = 300     #The only thing that should touch this variable, is the flywheel control program, and the physics equation

#DO NOT TOUCH U CAN DESTROY HARDWARE If you think this is an issue ask Gavin before changing stuff. (Gavin's Notes: Used for controlling startup and shutdown of flywheel)
startUp      = False #False is flywheel startup not complete, True is complete
Shutdown     = False #Used for shutting down flywheel
startUpRPM   = 200
internalRPM  = 0
RPMIncrement = 10
PIDIncrement = 10
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
# shooterActivate = False
#START ON ROLLER FOR AUTONOMOUS
start_on_roller = roller_orientation

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
    # intakeControl()
    
    
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
def ControllerGUI(row, text, var):
    Controller1.screen.clear_row(0)
    Controller1.screen.set_cursor(0,0)
    Controller1.screen.print(text, var)

#Threading-------------------------------------------------------#
def intakeControl():  #This is a intake control thread
    global intakeStatus, intakeSpeed
   
    if intakeStatus == True:
        Intake.spin(REVERSE, intakeSpeed, RPM)
    else:
        Intake.stop()

def flywheelStartup():
    global Shutdown
    global startUp
    Shutdown = False
    Flywheel.spin(FORWARD, Flywheel.velocity(VelocityUnits.RPM), VelocityUnits.RPM)
    internalRPM = Flywheel.velocity(VelocityUnits.RPM)
    while internalRPM <= startUpRPM:
        Flywheel.spin(FORWARD, internalRPM, VelocityUnits.RPM)
        internalRPM = internalRPM + RPMIncrement
        wait(RPMDelay, SECONDS)
    startUp = True

def flywheelShutdown():
    global Shutdown
    global startUp
    startUp = False
    Shutdown = True
    internalRPM = Flywheel.velocity(VelocityUnits.RPM)
    while internalRPM > 0:
        Flywheel.spin(FORWARD, internalRPM, VelocityUnits.RPM)
        internalRPM = internalRPM - RPMIncrement
        wait(RPMDelay, SECONDS)
    Flywheel.spin(FORWARD, 0, VelocityUnits.RPM)

def flywheelKeepSpeed():
    internalRPM = Flywheel.velocity(RPM)
    global flywheelTargetRpm
    #while internalRPM > flywheelTargetRpm + 10 or internalRPM < flywheelTargetRpm - 10:
    if startUp == True and Shutdown == False:
        if internalRPM < flywheelTargetRpm:
            internalRPM = internalRPM + PIDIncrement
            Flywheel.spin(FORWARD, internalRPM, VelocityUnits.RPM)
            brain.screen.set_cursor(10,0)
            brain.screen.clear_line()
            brain.screen.print("go up")
        else:
            internalRPM = internalRPM - PIDIncrement/2
            Flywheel.spin(FORWARD, internalRPM, VelocityUnits.RPM)
            brain.screen.set_cursor(10,0)
            brain.screen.clear_line()
            brain.screen.print("go down")
            

def Flywheel_TBH():
    global flyWheelTargetRpm
    gain = 1.0
    internalRPM = Flywheel.velocity(VelocityUnits.RPM)
    error = flywheelTargetRpm - internalRPM
    output = flywheelTargetRpm + gain*error
    Flywheel.spin(FORWARD, output, VelocityUnits.RPM)
    

def changeFlywheelSpeed1():
    global flywheelTargetRpm
    if flywheelTargetRpm > 100:
        flywheelTargetRpm = flywheelTargetRpm - 100
        

def changeFlywheelSpeed2():
    global flywheelTargetRpm
    if flywheelTargetRpm < 400:
        flywheelTargetRpm = flywheelTargetRpm + 100   


# #Driving Controls------------------------------------------------------------------#
#
#   INCLUDES
#
#   -SPEED CONTROLS
#   -MOTOR MOVEMENT
#   -TEST FUNCTION
#   -PNEUMATIC/EXPANSION
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#Driving Controls------------------------------------------------------------------#
def pneumaticRelease():
    pneumatic.open()

#Speed Settings-------------------------------------------#
def changeSpeedDown():
    global setSpeed
    setSpeed = 1
    ControllerGUI(0, "Speed", setSpeed)

def changeSpeedN():
    global setSpeed
    setSpeed = 3
    ControllerGUI(0, "Speed", setSpeed)

def changeSpeedUp():
    global setSpeed
    setSpeed = 4
    ControllerGUI(0, "Speed", setSpeed)
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
    pos = round(Controller1.axis2.position() / 1.5)
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
    pos1 = round(Controller1.axis3.position() / 1.5)
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
    global intakeStatus, intakeSpeed

    intakeStatus = not intakeStatus
    if intakeStatus == True:
        Intake.spin(FORWARD, 40, RPM)
    else:
        Intake.stop()
    
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

def driver_locator():
    locator()

def locator():
    while (True):
        x = None
        if(blue_team == False):
            x = visionSens.take_snapshot(RedSignature)
        else:
            x = visionSens.take_snapshot(BlueSignature)
        brain.screen.set_cursor(3,0)
        brain.screen.clear_line()
        brain.screen.print(x)

        if x != None:
            brain.screen.set_cursor(10,0)
            brain.screen.clear_line()
            print(x.centerX)
            if x.centerX+1 < 130:
                LHDrive.spin(REVERSE, 10)
                RHDrive.spin(FORWARD, 10)
                
            elif x.centerX+1 > 170:
                LHDrive.spin(FORWARD, 10)
                RHDrive.spin(REVERSE, 10)

            else:
                LHDrive.stop()
                RHDrive.stop()
                return True

        
        
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
    # driver_initialization()
    #LISTENS FOR A CHANGE IN JOYSTICKS
    Controller1.axis2.changed(moveMRight)
    Controller1.axis3.changed(moveMLeft)
    #ARROW BUTTONS TO CHANGE SPEED
    Controller1.buttonDown.pressed(changeSpeedDown)
    Controller1.buttonUp.pressed(changeSpeedUp)  
    #BUTTON TO TEST AUTONUM IN DRIVE MODE
    Controller1.buttonB.pressed(roller)
    Controller1.buttonY.pressed(driver_locator)
    Controller1.buttonX.pressed(pneumaticRelease)
    #Flywheel Speed Change
    Controller1.buttonLeft.pressed(changeFlywheelSpeed1)
    Controller1.buttonRight.pressed(changeFlywheelSpeed2)

    #buttons triggers
    #Flywheel Starting and shutting (left)
    Controller1.buttonL1.pressed(flywheelStartup)
    Controller1.buttonL2.pressed(flywheelShutdown)
    #Intake and Shooting (right)
    Controller1.buttonR1.pressed(intakeControl)
    Controller1.buttonR2.pressed(flywheelShoot)
    

    #turn on odometry
    while True:
        flywheelKeepSpeed()
        brain.screen.set_cursor(8,0)
        brain.screen.clear_row()
        brain.screen.print(Flywheel.velocity(), intakeStatus, flywheelTargetRpm, startUp, Shutdown)
        ControllerGUI(0, "Velocity", Flywheel.velocity())
        wait(100)

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
        LHDrive.spin(REVERSE, 15, RPM)
        RHDrive.spin(FORWARD, 15, RPM)
        if angle >= 2.36:
            break

    LHDrive.spin_for(FORWARD, 1080)
    RHDrive.spin_for(FORWARD, 1080)


    # Turn and shoot
    while(True):
        LHDrive.spin(REVERSE, 15, RPM)
        RHDrive.spin(FORWARD, 15, RPM)
        if angle >= 3.93:
            break
    

    flywheelShoot()
    wait(200)
    flywheelShoot()
    
def regular_start():
    # 10.21 # Measurement in INCHES
    
    global startUpRPM
        
    LHDrive.spin_for(FORWARD, 270, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = False)
    RHDrive.spin_for(FORWARD, 270, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = True)

    LHDrive.spin_for(REVERSE, 50, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = False)
    RHDrive.spin_for(FORWARD, 50, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = True)


    intakeButton()
    for i in range(3):
        LHDrive.spin_for(FORWARD, 60, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = False)
        RHDrive.spin_for(FORWARD, 60, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = True)
        LHDrive.spin_for(FORWARD, 30, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = False)
        RHDrive.spin_for(FORWARD, 30, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = True)
    intakeButton()
    
    LHDrive.spin_for(REVERSE, 100 , RotationUnits.DEG, 25, VelocityUnits.RPM, wait = False)
    RHDrive.spin_for(FORWARD, 100, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = True)
    
    locator()

    temp_startUpRPM = startUpRPM
    startUpRPM = 350
    
    flywheelStartup()
    wait(4000, MSEC)
    flywheelShoot()

    wait(7000, MSEC)
    flywheelShutdown()
    flywheelShoot()

    startUpRPM = temp_startUpRPM

def autonum():
    global start_on_roller


    # auton_inititialization()

    if start_on_roller:
        roller_start()
    else:
        regular_start()

comp = Competition(driver, autonum)
                                             