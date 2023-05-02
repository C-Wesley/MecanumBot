from motors import MotorController
from lidar import Lidar
from direction import DirectionManager
from controller import Controller

import RPi.GPIO as GPIO

import traceback
import math
import time


if __name__ == "__main__":
    
	GPIO.setmode(GPIO.BCM)
	controller = Controller()
	motors = MotorController()
	lidar = Lidar()
	directions = DirectionManager(5*math.pi/6, 7*math.pi/6, 300)

	# Set up 
	isJoystickProgram = 1
	button_state = 0
	p_button_state = 0

	while True: 
		button_state = controller.get_circle_button()

		if button_state != p_button_state:
			if button_state == 1: # Rising Edge
				isJoystickProgram = not isJoystickProgram
			p_button_state = button_state

		if isJoystickProgram:
			#joystickMainLoop()
			print("Joystick Control!")
		else:
			print("Autonomous Control!")
			