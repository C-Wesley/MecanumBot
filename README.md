# MecanumBot
Authors: Ryan Hoang and Wesley Cooke

This project was developed as a final project for Physics 3012 Electronics II at Augusta University.

![Overview Pic 1](https://github.com/C-Wesley/MecanumBot/blob/main/media/L298_pic.png "Overview 1")
![Overview Pic 2](https://github.com/C-Wesley/MecanumBot/blob/main/media/lidar_pic.png "Overview 2")

# Abstract
The purpose of this project is to utilize mecahnum wheels to remotely control a robot. The main computing element of the project is the Raspberry Pi 3 Model B. The motors were controlled using the L298 H-bridge. The first phase of the project involved mounting the mecanum wheels in the proper configuration. Next, the human interface device (HID) protocol was used to communicate with a PS4 controller. This provided access to the joystick values that were used to remotely control the robot. In addition to controlling the robot with the controller, two autonomous movement algorithms were developed to control the robot using lidar. The first algorithm, "Parallel Wall Algorithm," is designed to ensure the robot is parallel with the left wall. Note an assumption is that the left wall exist while this algorithm is active. The second algorithm, "Wall Distance Contraint Algorithm," extends the "Parallel Wall Algorithm" by adding a upper and lower bound on the distance from the wall. This means that the robot will attempt to become parallel with the wall while also getting within a certain distance of it. The testing of these algorithms show that they do work, but there are some limitations. The lidar takes time to collect data, and it doesn't always return the distances at the angles needed. To combat this issue, we have limited the max power of the robot for the autonomous demonstrations. 

# Mecanum Wheels

![Birds Eye View of the robot](https://github.com/C-Wesley/MecanumBot/blob/main/media/topView_wheels.jpg "Top View")
![Worms Eye View of the robot](https://github.com/C-Wesley/MecanumBot/blob/main/media/bottomView_wheels.jpg "Bottom View")

The important thing to note about the mounting of the mecanum wheels is that from a birds eye view, the wheels should form an X. From the worms view, this will be the opposite. This is needed to ensure that the direction of force is in the proper direction.

This diagram showcases the direction of the force vectors. Notice that the unit vectors for these wheels can have sideways and diagonal movements. 

![Force Vector Directions](https://github.com/C-Wesley/MecanumBot/blob/main/media/mecanumWheel_directions.png "Force Directions")

# HID with PS4 
This picture is the data from the HID report. It is in a string of bytes. These values are then casted to a list in order to extract out certain bytes or bits as required. More information can be found here: [HID Byte Map]https://www.psdevwiki.com/ps4/DS4-USB

![PS4 HID Data](https://github.com/C-Wesley/MecanumBot/blob/main/media/ps4_hid.png "PS4 HID Data")

# Joystick Control 
The general power equation used for the motors control is the following: Power = magnitude * sin(angle +- π/4). The magnitude of the x and y components of the joystick is used to power the motors. The arctangent of the x and y components of the joystick is used to calculate the angle which dictates the direction of movement. However, since the force vector for each motor is off by either + π/4 or - π/4, it is added to the angle to generate the correct movement for the vehicle. 

![Diagram of a vector with x and y component](https://github.com/C-Wesley/MecanumBot/blob/main/media/joystick_diagram.png "Vector Diagram")

# Power Delivery 
The Raspberry Pi 3 Model B needs about 3 amps of current. To deliver the power to the Raspberry Pi 3 Model B, the LM338 is used. It is an adjustable regulator capable of supplying up to 5 amps. A voltage divider setup was used to get ~5 volts for the output. Although one can be used for this project, three of them were used in parallel to help with heat dissapation. A circuit diagram is presented below. 

![LM338 Circuit Diagram](https://github.com/C-Wesley/MecanumBot/blob/main/media/power_delivery.png "LM338 Circuit Diagram")

# Autonomous Algorithms
For both autonomous algorithms, the following assumptions were made: assume angle 0 is the right side of the robot, angle 90 is the front of the robot, angle 180 is the left of the robot, and angle 270 is the back. 

## Parallel Wall Algorithm
To ensure the robot is parallel to the left wall, two angle bounds, 5π/6 and 7π/6, were used to center the robot with respect to the wall. The algorithm monitors the distance at the angles 5π/6 (call this A) and 7π/6 (call this B) using the lidar technology. This forms a triangle between the center of the lidar and the points on the wall. There are 3 cases to consider. If A = B (distances are the same at the angle bounds) the robot is parallel with the wall and will continue to move forwards. If A > B, then the robot is moving to the right. The algorithm will turn the heading of the car towards the left, moving it to the left. If A < B, then the robot is moving left and will turn its heading of the car towards the right, moving it to the right. 

![Parallel Wall Algorithm](https://github.com/C-Wesley/MecanumBot/blob/main/media/parallel_wall_diagram.png "Parallel Wall Algorithm")

## Wall Distance Constraint Algorithm
To add a wall distance contraint, this algorithm includes code to monitor the distance at π. The distance is referred to as Xw in the picture. The algorithm also has two hardcoded distance bounds, upperbound and lowerbound. They are referred to as X2 and X1 respectively in the picture. Additionally two angle bounds, 5π/6 and 7π/6, were used to center the robot with respect to the wall. The algorithm monitors the distance at the angles 5π/6 (call this A) and 7π/6 (call this B) using the lidar technology. There are 3 cases to consider. If Xw is between the upper and lowerbound, the car will continue to move straight. If Xw is less than the lowerbound, the robot will go right. If Xw is greater than the upperbound, the robot will go left. This algorithm takes advantage of the diagonal movement of the mechanum wheels. Assume for this scenario, the robot wants to follow the wall. When Xw is within the lower and upperbound, the robot will go straight. If the robot is not within the bounds, theta is calculated using using A and Xw. Depending on the case theta is either then added or subtracted to π/2, causing the robot to move in a strafe motion towards the lower and upperbounds.

![Wall Distance Constraint Algorithm](https://github.com/C-Wesley/MecanumBot/blob/main/media/wall_constraint_diagram.png "Wall Distance Contraint Algorithm")

# Demos 

## Joystick Demo
![Joystick Demo](https://github.com/C-Wesley/MecanumBot/blob/main/media/gifs/joystick.gif "Joystick Demo")

## Parallel Wall Algorithm Demos
![Parallel Wall Alg Demo 1](https://github.com/C-Wesley/MecanumBot/blob/main/media/gifs/parallel_1.gif "Parallel Wall Alg Demo 1")
![Parallel Wall Alg Demo 2](https://github.com/C-Wesley/MecanumBot/blob/main/media/gifs/parallel_2.gif "Parallel Wall Alg Demo 2")
![Parallel Wall Alg Demo 3](https://github.com/C-Wesley/MecanumBot/blob/main/media/gifs/parallel_3.gif "Parallel Wall Alg Demo 3")
## Wall Constraint Algorithm Demos
![Wall Constraint Alg Demo 1](https://github.com/C-Wesley/MecanumBot/blob/main/media/gifs/wall_1.gif "Wall Constraint Alg Demo 1")
![Wall Constraint Alg Demo 2](https://github.com/C-Wesley/MecanumBot/blob/main/media/gifs/wall_2.gif "Wall Constraint Alg Demo 2")
