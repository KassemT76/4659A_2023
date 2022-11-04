# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       gavin                                                        #
# 	Created:      2022-11-03, 8:08:19 p.m.                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

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
Flywheel1      = vex.Motor(vex.Ports.PORT11, vex.GearSetting.RATIO_36_1, True  )    #Direct Couple to internal motor shaft
Flywheel2      = vex.Motor(vex.Ports.PORT12, vex.GearSetting.RATIO_36_1, False )
Intake         = vex.Motor(vex.Ports.PORT13, vex.GearSetting.RATIO_36_1, True  )    #Not Finalized
Rollers        = vex.Motor(vex.Ports.PORT21, vex.GearSetting.RATIO_18_1, False )    #Not Finalized
LFMotor        = vex.Motor(vex.Ports.PORT15, vex.GearSetting.RATIO_6_1 , False )
LRMotor        = vex.Motor(vex.Ports.PORT18, vex.GearSetting.RATIO_6_1 , False )
RFMotor        = vex.Motor(vex.Ports.PORT19, vex.GearSetting.RATIO_6_1 , True  )
RRMotor        = vex.Motor(vex.Ports.PORT20, vex.GearSetting.RATIO_6_1 , False )


#Motor Grouping---------------------------------------------------#
LHDrive  = vex.MotorGroup(LFMotor, LRMotor)
RHDrive  = vex.MotorGroup(RFMotor, RRMotor)
Flywheel = vex.MotorGroup(Flywheel1, Flywheel2)


def compStart():
   Intake.set_velocity(100, )

