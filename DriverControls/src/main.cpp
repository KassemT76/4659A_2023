// ---- START VEXCODE CONFIGURED DEVICES ----
// Robot Configuration:
// [Name]               [Type]        [Port(s)]
// motorsLeft           motor_group   1, 2            
// motorsRight          motor_group   3, 4            
// Controller1          controller                    
// ---- END VEXCODE CONFIGURED DEVICES ----
// ---- START VEXCODE CONFIGURED DEVICES ----
// Robot Configuration:
// [Name]               [Type]        [Port(s)]
// motorsLeft           motor_group   1, 2            
// motorsRight          motor_group   3, 4            
// Controller1          controller                    
// ---- END VEXCODE CONFIGURED DEVICES ----
/*----------------------------------------------------------------------------*/
/*                                                                            */
/*    Module:       main.cpp                                                  */
/*    Author:       C:\Users\super                                            */
/*    Created:      Thu Oct 06 2022                                           */
/*    Description:  V5 project                                                */
/*                                                                            */
/*----------------------------------------------------------------------------*/

// ---- START VEXCODE CONFIGURED DEVICES ----
// Robot Configuration:
// [Name]               [Type]        [Port(s)]
// motorsLeft           motor_group   1, 2            
// motorsRight          motor_group   3, 4            
// Controller1          controller                    
// ---- END VEXCODE CONFIGURED DEVICES ----

#include "vex.h"

using namespace vex;

void axis1(); 
void axis2();
void axis3();
void axis4();

int main() {
  // Initializing Robot Configuration. DO NOT REMOVE!
  vexcodeInit();
  //listens for any changes to joysticks
  Controller1.Axis1.changed(axis1);
  Controller1.Axis2.changed(axis2);
  Controller1.Axis3.changed(axis3);
  Controller1.Axis4.changed(axis4);
}


// *experimental changes
// motorsLeft are controlled by the left joystick
// motorsRight are now controlled by right joystick


//left and right on right joystick
void axis1(){
  
}

//up and down on right joystick
void axis2(){
  float pos = Controller1.Axis2.position(percent);
  Brain.Screen.clearLine();
  Brain.Screen.print("A2: ");
  Brain.Screen.print(pos); 

  if (pos < 0)
  {
    motorsRight.spin(reverse);
    motorsRight.setVelocity(pos, percent);
  }
  else 
  {
    motorsRight.spin(forward);
    motorsRight.setVelocity(pos, percent);
  }
}

//up and down on left joy

void axis3(){
  float pos = Controller1.Axis3.position(percent);

  if (pos < 0){
    motorsLeft.spin(reverse);
    // motorsRight.spin(reverse);
    motorsLeft.setVelocity(pos, percent);
    // motorsRight.setVelocity(pos, percent);
  }
  else {
    motorsLeft.spin(forward);
    // motorsRight.spin(forward);
    motorsLeft.setVelocity(pos, percent);
    // motorsRight.setVelocity(pos, percent);
  }

  Brain.Screen.clearLine();
  Brain.Screen.print("A3: ");
  Brain.Screen.print(pos); 
}


void axis4(){
 
}