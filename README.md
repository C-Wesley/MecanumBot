# MecanumBot
Authors: Ryan Hoang and Wesley Cooke

This project was developed as a final project for the Electronics II course at Augusta University.

# Abstract
The purpose of this project is to utilize mecahnum wheels to remotely control a robot. The main computing element of the project is the Raspberry Pi 3b. The motors were controlled using the L298 H-bridge. The first phase of the project involved mounting the mecanum wheels in the proper configuration. Next, we used the human interface device (HID) protocol to communicate with a PS4 controller in our program.This provided access to the joystick values that we used to remotely control the robot. After implementing the control using the joystick, we developed a few autonomous algorithms to control the robot. The first algorithm is designed to ensure the robot is parallel with a wall to it's left. We make the assumption that the left wall is there. We call this the "parallel wall algorithm". The second algorithm extends the "parallel wall algorithm" by adding a upper and lower bound on the distance from the wall. This means that the robot will attempt to become parallel with the wall while also getting within a certain distance of it. We call this the "wall distance contraint algorithm". The testing of these algorithms show that they do work. However, the lidar takes time to collect data, and it doesn't always return the distance at the angles needed. To combat this issue, we have limited the max power of the robot for the autonomous demonstrations. 

# Mecanum Wheels
![Birds Eye View of the robot](https://raw.githubusercontent.com/C-Wesley/MecanumBot/main/media/topView_wheels.jpg "Top View")
![Worms Eye View of the robot](https://(https://raw.githubusercontent.com/C-Wesley/MecanumBot/main/media/bottomView_wheels.jpg "Bottom View")
The import thing to note about the mounting of the mecanum wheels is that from a birds eye view, the wheels should form an X. From the worms view, this will look opposite. However, this is very important to get right to ensure the the direction of force is in the proper direction.

In this diagram, you can see the direction of the force vectors. Notice that if you resolve some unit vectors, completely sideways movement, and diagonal movements are possible. 
![Force Vector Directions](https://raw.githubusercontent.com/C-Wesley/MecanumBot/main/media/mecanumWheel_directions.png "Force Directions")

# HID with PS4 
This is what the data we receive from the HID report looks like. It is a bytes data type that we can cast to a list and pick out bytes or bits as required. Consult the following map for more information: [HID Byte Map]https://www.psdevwiki.com/ps4/DS4-USB
![PS4 HID Data]([https://](https://raw.githubusercontent.com/C-Wesley/MecanumBot/main/media/bottomView_wheels.jpg "PS4 HID Data")

# Joystick Control 
We are using the magnitude of the x and y components of the joystick as the power to the motors. However, since the force vector for each motor is off by + or - pi/4, we multiply by sin(atan2(y/x) + or - pi/4) for each motor. Which motor dictates if it is +pi/4 or -pi/4.  
![Diagram of a vector with x and y component](https://raw.githubusercontent.com/C-Wesley/MecanumBot/main/media/joystick_diagram.png "Vector Diagram")

# Power Delivery 
To Deliver the power to the Raspberry Pi 3, we are using an LM338. This is an adjustable regulator capable of supplying up to 5A. We have three of them in parallel to help with heat dissapation. 
![LM338 Circuit Diagram](https://raw.githubusercontent.com/C-Wesley/MecanumBot/main/media/power_delivery.png "LM338 Circuit Diagram")

# Autonomous Algorithms
For these algorithms, Assume angle 0 is the right side of the robot, angle 90 is the front of the robot, angle 180 is the left of the robot, and angle 270 is the back. 

## Parallel Wall Algorithm
To ensure the robot is parallel to the left wall, we are monitoring the distance at the angles 150 degrees (call this A) and 210 degrees (call this B) using the lidar. This forms a triangle between the center of the lidar and the points on the wall. We know that the robot is parallel with the wall if A = B. If A > B, then the robot is looking right and needs to turn back left. If A < B, then the robot is looking left and needs to trun back right. 

## Wall Distance Constraint Algorithm
To add a wall distance contraint, we begin monitoring the distance at 180 degrees (call this Xw). If Xw is between our upper and lower bound, we are good. If Xw is < lower bound, we need to go right. If Xw is > Upper bound, we need to go left. We do this by taking advantage of the diagonal movemnet of the robot. Assume we want to follow the wall, therefore, when our Xw is within the lower and upper bound, we direct the robot to go straight. If we are not within the bound, we calculate theta using A and Xw. Then we subtract or add this theta to 90 depending on the case. This causes a strafe movement towards the lower and upper bounds.

# Demos 

