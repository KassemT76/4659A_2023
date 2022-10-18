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

//left and right on right joystick
void axis1(){
  //variable "pos" is position of joystick
  float pos = Controller1.Axis1.position(percent);

  //pos < 0 is left
  if (pos < 0){
    //turns the robot left
    motorsLeft.spin(reverse);
    motorsRight.spin(forward);
    motorsLeft.setVelocity(pos, percent);
    motorsRight.setVelocity(pos, percent);
  }
  //if it isnt (pos < 0)turn right
  else{
    motorsLeft.spin(forward);
    motorsRight.spin(reverse);
    motorsLeft.setVelocity(pos, percent);
    motorsRight.setVelocity(pos, percent);
  }
  Brain.Screen.clearLine();
  Brain.Screen.print("A1: ");
  Brain.Screen.print(pos); 
  
  
}

//up and down on right joystick
void axis2(){
  float pos = Controller1.Axis2.position(percent);
  Brain.Screen.clearLine();
  Brain.Screen.print("A2: ");
  Brain.Screen.print(pos); 
  
  
}

//up and down on left joy
void axis3(){
  float pos = Controller1.Axis3.position(percent);

  if (pos < 0){
    motorsLeft.spin(reverse);
    motorsRight.spin(reverse);
    motorsLeft.setVelocity(pos, percent);
    motorsRight.setVelocity(pos, percent);
  }
  else {
    motorsLeft.spin(forward);
    motorsRight.spin(forward);
    motorsLeft.setVelocity(pos, percent);
    motorsRight.setVelocity(pos, percent);
  }

  Brain.Screen.clearLine();
  Brain.Screen.print("A3: ");
  Brain.Screen.print(pos); 
  
  
  
}

//right and left left joy
void axis4(){
  float pos = Controller1.Axis4.position(percent);

  //when he turns left you turn left
  if (pos > 0){
    motorsRight.stop();
    motorsLeft.spin(forward);
    motorsLeft.setVelocity(pos, percent);
  }
  else{
    motorsLeft.stop();
    motorsRight.spin(forward);
    motorsRight.setVelocity(pos, percent);

  }

  Brain.Screen.clearLine();
  Brain.Screen.print("A4: ");
  Brain.Screen.print(pos); 
  
}