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

# PREGAME CONFIG -----------------------------------------------------------------#
#
# INCLUDES
#
# - Team Colour
# - Robot Orientation
#  # # # # # # # # # # # # # # # # # #

blue_team =  True
start_on_roller = False

offset = 8
lowerBound = 147
upperBound = 153
integral = 0
prev_error = 0

# CONFIGURATION ------------------------------------------------------------------#
#
#   INCLUDES
#
#   -Variable Definitions
#   -Calibration
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if blue_team:
    opp_team = Color.RED 
    team = Color.BLUE 
    #Blue seen with sensor = Color("00FFFF")
else:
    opp_team = Color.BLUE # 
    team =  Color.RED 

brain          = Brain()
Screen         = brain.screen
Controller1    = Controller()

Flywheel      = Motor(Ports.PORT9, GearSetting.RATIO_6_1  , False  )    #Do not change gear ratio

Intake         = Motor(Ports.PORT8, GearSetting.RATIO_18_1 , True  )    

LFFMotor       = Motor(Ports.PORT5, GearSetting.RATIO_36_1 , False )
LFMotor        = Motor(Ports.PORT1, GearSetting.RATIO_36_1 , True )
LRMotor        = Motor(Ports.PORT2, GearSetting.RATIO_36_1 , True )

RFFMotor       = Motor(Ports.PORT6, GearSetting.RATIO_36_1 , True )
RFMotor        = Motor(Ports.PORT3, GearSetting.RATIO_36_1 , False  )
RRMotor        = Motor(Ports.PORT4, GearSetting.RATIO_36_1 , False )

RedSignature = Signature(1, 3201, 9325, 6264, -1117, 295, -412, 1.200, 0)
BlueSignature = Signature(2, -3133, 817, -1158, 249, 8683, 4466, 0.600, 0)

opticSens = Optical(Ports.PORT11)
visionSens = Vision(Ports.PORT10, 90, RedSignature, BlueSignature)

pneumatic = Pneumatics(brain.three_wire_port.h)

#Program Internal Constants--------(Don't screw arround with this if you don't know what you are doing.)-----------#
intakeStatus = False   #Switch for turning on and off intake. Set this variable to False in your code if u wanna switch it off.
flywheelTargetRpm  = 200     #The only thing that should touch this variable, is the flywheel control program, and the physics equation
#DO NOT TOUCH U CAN DESTROY HARDWARE If you think this is an issue ask Gavin before changing stuff. (Gavin's Notes: Used for controlling startup and shutdown of flywheel)
startUp      = False #False is flywheel startup not complete, True is complete
Shutdown     = False #Used for shutting down flywheel
startUpRPM   = 200
RPMIncrement = 10
setSpeed     = 2
RPMDelay     = 0.025

#Intake
intakeSpeed = 200

#Motor Grouping---------------------------------------------------#
RHDrive  = MotorGroup(RFFMotor, RFMotor, RRMotor)
LHDrive  = MotorGroup(LFFMotor, LFMotor, LRMotor)

#First print
Screen.print("Program Loaded!")
#Information header
Screen.clear_line()
Screen.set_cursor(1,0)
Screen.print("Information: ")

def initialization():  
    pneumatic.close()
    
def driver_initialization():
    global startUp
    global intakeStatus
    
    initialization()

    startUp = False
    flywheelStartup()
    
def auton_inititialization():
    global startUp
    global intakeStatus
    
    initialization()

    startUp = False
    flywheelStartup()


def shutDown():
    LHDrive.stop()
    RHDrive.stop()
    Intake.stop()
    flywheelShutdown()

# Low Level Services ------------------------------------------------------------------#
#
#   INCLUDES
#   -GUI
#   -Odometry
#   -PID controls
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ControllerGUI(text, var):
    Controller1.screen.clear_row(0)
    Controller1.screen.set_cursor(0,0)
    Controller1.screen.print(text, var)

def logger(row, text, var):
    Screen.clear_row(row)
    Screen.set_cursor(row,0)
    Screen.print(text, var)

def buttons():
    Screen.draw_rectangle(100, 100, 100, 50, Color.RED)
    Screen.draw_rectangle(250, 100, 100, 50, Color.BLUE)

def buttonPressed():
    global blue_team
    if Screen.x_position() > 100 and Screen.x_position() < 200 and Screen.y_position() > 100 and Screen.y_position() < 150: 
        logger(4,"Red", Screen.x_position())
        blue_team = False
    if Screen.x_position() > 250 and Screen.x_position() < 350 and Screen.y_position() > 100 and Screen.y_position() < 150: 
        logger(5,"Blue", Screen.x_position())
        blue_team = True

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

def pid_control(target_rpm, current_rpm, Kp, Ki, Kd, dt):
    global integral, prev_error
    error = target_rpm - current_rpm
    integral = integral + error * dt
    derivative = (error - prev_error) / dt
    output = Kp * error + Ki * integral + Kd * derivative
    prev_error = error
    return output

def flywheelKeepSpeed():
    global flywheelTargetRpm
    if startUp == True and Shutdown == False:
        Flywheel.set_velocity(pid_control(flywheelTargetRpm,Flywheel.velocity(),1,0.1,0.1,0.01), VelocityUnits.RPM)
        

def changeFlywheelSpeedDecrease():
    global flywheelTargetRpm
    if flywheelTargetRpm > 50:
        flywheelTargetRpm = flywheelTargetRpm - 50
        

def changeFlywheelSpeedIncrease():
    global flywheelTargetRpm
    if flywheelTargetRpm < 400:
        flywheelTargetRpm = flywheelTargetRpm + 50   


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
    if setSpeed >= 1:
        setSpeed += 1
    ControllerGUI("Speed", setSpeed)

def changeSpeedUp():
    global setSpeed
    if setSpeed <= 4:
        setSpeed -= 1
    ControllerGUI("Speed", setSpeed)
#Moving the motors----------------------------------------#

#IS CALLED WHEN AXIS2 (RIGHT JOYSTICK - VERTICAL) IS CHANGED
def moveDrivetrain():
   LHDrive.spin(FORWARD, (Controller1.axis3.position()+Controller1.axis1.position()/2)*0.25*setSpeed, VelocityUnits.PERCENT)
   RHDrive.spin(FORWARD, (Controller1.axis3.position()-Controller1.axis1.position()/2)*0.25*setSpeed, VelocityUnits.PERCENT)

def intakeButton():
    global intakeStatus

    intakeStatus = not(intakeStatus)
    intakeControl()

def flywheelShoot():
    global intakeStatus, intakeSpeed

    intakeStatus = not(intakeStatus)
    if intakeStatus == True:
        Intake.spin(FORWARD, 75, RPM)
    else:
        Intake.stop()

def driver_locator():
    refined_locator()

# #Autonum Controls------------------------------------------------------------------#
#
#   INCLUDES
#
#   -ROLLER MOVEMENT
#   -Vision sensors
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def roller():
    global opp_team, team, intakeSpeed
    opticColor = opticSens.color() 
    

    if opticColor == opp_team:
        Intake.spin(FORWARD, intakeSpeed, RPM)   

    Screen.set_cursor(9,0)
    Screen.clear_line()
    Screen.print("Color ", opticColor, opp_team, team)

    if opticColor == team:
        # CHANGE TO NOT INTERFERE WITH INDEXER
        Intake.stop()
    wait(50)
def refined_locator():
    i = 0
    leftBound = 20
    rightBound = 280
    while (True):
        if(blue_team):
            x = visionSens.take_snapshot(BlueSignature)
        else:
            x = visionSens.take_snapshot(RedSignature)
        
        if x != None:
            logger(10, "Camera", x)
            if not(x[i].exists):
                    logger(5, "Not exists", x[i-1])
                    break
            if x[i].centerX < leftBound or x[i].centerX > rightBound:
                i+=1
            if x[i].centerX+offset < lowerBound:
                LHDrive.spin(REVERSE, 10)
                RHDrive.spin(FORWARD, 10)
                if rightBound > upperBound:
                    rightBound -= 10
                
            elif x[i].centerX+offset > upperBound:
                LHDrive.spin(FORWARD, 10)
                RHDrive.spin(REVERSE, 10)
                if leftBound > lowerBound:
                    leftBound += 10

            else:
                LHDrive.stop()
                RHDrive.stop()
                return True
            wait(250, MSEC)
def locator():
    global offset, upperBound, lowerBound
    while (True):
        if(blue_team):
            x = visionSens.take_snapshot(BlueSignature)
        else:
            x = visionSens.take_snapshot(RedSignature)
        logger(5, "Did it detect?", x)
        if x != None:
            logger(10, "Camera", x)
            if x[0].centerX+offset < lowerBound:
                LHDrive.spin(REVERSE, 10)
                RHDrive.spin(FORWARD, 10)
                
            elif x[0].centerX+offset > upperBound:
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
    global flywheelTargetRpm

    driver_initialization()

    Controller1.axis1.changed(moveDrivetrain)
    #ARROW BUTTONS TO CHANGE SPEED
    Controller1.buttonDown.pressed(changeSpeedDown)
    Controller1.buttonUp.pressed(changeSpeedUp)  
    #BUTTON TO TEST AUTONUM IN DRIVE MODE
    Controller1.buttonB.pressed(roller)
    Controller1.buttonY.pressed(driver_locator)
    Controller1.buttonX.pressed(pneumaticRelease)
    #Flywheel Speed Change
    Controller1.buttonLeft.pressed(changeFlywheelSpeedDecrease) 
    Controller1.buttonRight.pressed(changeFlywheelSpeedIncrease)

    #buttons triggers
    #Flywheel Starting and shutting (left)
    Controller1.buttonL1.pressed(flywheelStartup)
    Controller1.buttonL2.pressed(flywheelShutdown)
    #Intake and Shooting (right)
    Controller1.buttonR1.pressed(intakeButton)
    Controller1.buttonR2.pressed(flywheelShoot)

    buttons()
    #turn on odometry
    while True:
        flywheelKeepSpeed()
        moveDrivetrain()
        buttonPressed()

        Screen.set_cursor(3,0)
        Screen.clear_row()
        Screen.print(Flywheel.velocity(), intakeStatus, flywheelTargetRpm, startUp, Shutdown)

        ControllerGUI("Velocity", round(Flywheel.velocity()))

        Controller1.screen.print(" ", flywheelTargetRpm, setSpeed)

        wait(100)

def autonum():
    global start_on_roller
 
    auton_inititialization()
    if start_on_roller:
        roller_start()
    else:
        regular_start()

def roller_start():
    roller()
    
def regular_start():
    # 10.21 # Measurement in INCHES
    
    global startUpRPM
    global intakeStatus

    temp_startUpRPM = startUpRPM
    startUpRPM = 350
    
    flywheelStartup()

    LHDrive.spin_for(FORWARD, 270, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = False)
    RHDrive.spin_for(FORWARD, 270, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = True)

    LHDrive.spin_for(REVERSE, 55, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = False)
    RHDrive.spin_for(FORWARD, 55, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = True)


    intakeButton()
    for i in range(3):
        LHDrive.spin_for(FORWARD, 60, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = False)
        RHDrive.spin_for(FORWARD, 60, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = True)
        LHDrive.spin_for(FORWARD, 30, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = False)
        RHDrive.spin_for(FORWARD, 30, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = True)
    intakeButton()
    
    LHDrive.spin_for(REVERSE, 120 , RotationUnits.DEG, 25, VelocityUnits.RPM, wait = False)
    RHDrive.spin_for(FORWARD, 120, RotationUnits.DEG, 25, VelocityUnits.RPM, wait = True)
    
    refined_locator()
    logger(9, "Done", intakeStatus)
    intakeStatus = False
    flywheelShoot()

    flywheelShutdown()

    startUpRPM = temp_startUpRPM

comp = Competition(driver, autonum)