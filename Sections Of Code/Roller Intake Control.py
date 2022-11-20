from vex import *

#Global Control Varibles

teamColor = True    #True is team Red, False  is team Blue

#Intake/Roller Control Variables
intakeMode = True  #True is regular intake/indexer, False is Roller mode
intakeStatus = False   #True is intake on, False is  intake off
intakeRPM    = 600
wallDistance = 10



#Temp for testing
brain          = Brain()
Controller1    = Controller()
Intake         = Motor(Ports.PORT13, GearSetting.RATIO_6_1  , True  )


def intakeControl():  #Intake control thread
    while True:
        if intakeStatus == True:
            if intakeMode == True:
                #Intake Mode
                Intake.spin(FORWARD, intakeRPM, RPM)

            else: 
                print('RollerMode')
                Intake.spin(FORWARD, 0, RPM)

        else: 
            Intake.spin(FORWARD, 0  , RPM)


#Temp PROGRAM TEST CONTROLS
def changeSpeedDown():
    global intakeStatus
    intakeStatus = False
    print("Down")
    
def changeSpeedN():
    global intakeMode
    intakeMode = False
    print("Right")
    
def changeSpeedT():
    global intakeMode
    intakeMode = True
    print("Left")
    
    
def changeSpeedUp():
    global intakeStatus
    intakeStatus = True
    print("Up")
    

my_thread1 = Thread(intakeControl)

def driver():
    Controller1.buttonDown.pressed(changeSpeedDown)
    Controller1.buttonUp.pressed(changeSpeedUp)  
    Controller1.buttonRight.pressed(changeSpeedN)
    Controller1.buttonLeft.pressed(changeSpeedT)

def autonum():
    print("lol")

comp = Competition(driver, autonum)