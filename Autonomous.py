from motors import MotorController
from lidar import Lidar
from direction import DirectionManager
import RPi.GPIO as GPIO
import time

import math

if __name__ == "__main__":
	
	GPIO.setmode(GPIO.BCM)
	motors = MotorController()
	lidar = Lidar()
	directions = DirectionManager(math.pi/6, 5*math.pi/6, 300)
	num_scans = 5
	
	running = True
	while running:
		try:
			# make sure we are stationary 
			motors.stopAllMotors()
			
			# Get some scans
			scans = lidar.scan(num_scans)

			# Process the scans 
			directions.filter_scans(scans)
			
			# Get the variables we need to make decisions with 
			angle = directions.get_angle_with_max_distance()
			min_distance = directions.get_min_distance()
			
			# Print stuff
			print(angle*180/math.pi)
			print(min_distance)
			
			mag = 0.5
			power1 = 100*(math.sin(angle-(1/4)*math.pi)*mag)
			power2 = 100*(math.sin(angle+(1/4)*math.pi)*mag)
			
			if min_distance <= directions.disThres:
				motors.stopAllMotors()
			else:
				motors.setMotorPower(motors.forwardA, motors.backwardA, motors.pwmA, power1)
				motors.setMotorPower(motors.forwardB, motors.backwardB, motors.pwmB, power2)
				motors.setMotorPower(motors.forwardC, motors.backwardC, motors.pwmC, power1)
				motors.setMotorPower(motors.forwardD, motors.backwardD, motors.pwmD, power2)
			
			time.sleep(1)
		
		except KeyboardInterrupt:
			print("Exiting for keyboard interrupt")
			motors.cleanup()
			lidar.disconnect()
			running = False
		
		except Exception as e:
			print(e)
			lidar.disconnect()
			
			
