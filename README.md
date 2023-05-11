# MecanumBot
Authors: Ryan Hoang and Wesley Cooke

This project was developed as a final project for the Electronics II course at Augusta University.

# Abstract
The purpose of this project is to utilize mecahnum wheels to remotely control a robot. The main computing element of the project is the Raspberry Pi 3b. The motors were controlled using the L298 H-bridge. The first phase of the project involved mounting the mecanum wheels in the proper configuration. Next, we used the human interface device (HID) protocol to communicate with a PS4 controller in our program.This provided access to the joystick values that we used to remotely control the robot. After implementing the control using the joystick, we developed a few autonomous algorithms to control the robot. The first algorithm is designed to ensure the robot is parallel with a wall to it's left. We make the assumption that the left wall is there. We call this the "parallel wall algorithm". The second algorithm extends the "parallel wall algorithm" by adding a upper and lower bound on the distance from the wall. This means that the robot will attempt to become parallel with the wall while also getting within a certain distance of it. We call this the "wall distance contraint algorithm". The testing of these algorithms show that they do work. However, the lidar takes time to collect data, and it doesn't always return the distance at the angles needed. To combat this issue, we have limited the max power of the robot for the autonomous demonstrations. 

# Mecanum Wheels
![Alt text](https://raw.githubusercontent.com/C-Wesley/MecanumBot/main/media/topView_wheels.jpg?token=GHSAT0AAAAAACBYYWVLCWYLC763MUOHQGXIZC5ID5A "Top View")
![Alt text]([https://](https://raw.githubusercontent.com/C-Wesley/MecanumBot/main/media/bottomView_wheels.jpg?token=GHSAT0AAAAAACBYYWVK6W6EKL3E5GAY35NQZC5IEKA "Bottom View")

# HID with PS4 

# Joystick Control 

# Power Delivery 

# Autonomous Algorithms

# Demos 

