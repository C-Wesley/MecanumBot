from motors import MotorController
from lidar import Lidar
from direction import DirectionManager
import RPi.GPIO as GPIO
import traceback
import time

import math

if __name__ == "__main__":
	
	GPIO.setmode(GPIO.BCM)
	motors = MotorController()
	lidar = Lidar()
	directions = DirectionManager(5*math.pi/6, 7*math.pi/6, 300)
	num_scans = 5
	turn = 0

	running = True
	while running:
		try:
			# make sure we are stationary
			#motors.stopAllMotors()
			
			# Get some scans
			scans = lidar.scan(num_scans)

			# Process the scans 
			directions.filter_scansAlg(scans)
			# Get the variables we need to make decisions with 
			print(directions.filteredScansAngle)
			
			upperDistance = directions.filteredScansAngle.get(int(directions.upperBound*(180/math.pi)), 0)
			lowerDistance = directions.filteredScansAngle.get(int(directions.lowerBound*(180/math.pi)), 0)
			
			print(upperDistance)
			print(lowerDistance)
			mag = 0.25

			#Include turn
			if upperDistance != 0 and lowerDistance != 0:
				
				turn = (upperDistance-lowerDistance)/max(upperDistance,lowerDistance)
				turn = turn/4
				#if(upperDistance > lowerDistance):
				#	turn = (upperDistance - lowerDistance)/max(upperDistance,lowerDistance)
				#elif(upperDistance < lowerDistance):
					#turn = (lowerDistance - upperDistance)/max(upperDistance,lowerDistance)
				
					
				print(turn)
				power1 = (math.sin((math.pi/2)-(1/4)*math.pi))
				power2 = (math.sin((math.pi/2)+(1/4)*math.pi)) 
				
				our_max = max(abs(power1), abs(power2))
				a_power = mag*power2/our_max + turn
				b_power = mag*power1/our_max - turn
				d_power = mag*power1/our_max + turn
				c_power = mag*power2/our_max - turn
				
				
				
				if (mag + abs(turn) > 1):
					a_power /= mag + abs(turn)
					b_power /= mag + abs(turn)
					c_power /= mag + abs(turn)
					d_power /= mag + abs(turn)
				
				a_power *= 100
				b_power *= 100
				c_power *= 100
				d_power *= 100
			
			
				"""			print(f"Angle: {angle}")
				print(f"a_power: {a_power}") 
				print(f"b_power: {b_power}") 
				print(f"c_power: {c_power}")
				print(f"d_power: {d_power}") 
				
				"""
			

				motors.setMotorPower(motors.forwardA, motors.backwardA, motors.pwmA, a_power)
				motors.setMotorPower(motors.forwardB, motors.backwardB, motors.pwmB, b_power)
				motors.setMotorPower(motors.forwardC, motors.backwardC, motors.pwmC, c_power)
				motors.setMotorPower(motors.forwardD, motors.backwardD, motors.pwmD, d_power)

			else:
				turn = 0
			
			time.sleep(0.1)
		
			
		except KeyboardInterrupt:
			print("Exiting for keyboard interrupt")
			motors.cleanup()
			lidar.disconnect()
			running = False
		
		except Exception as e:
			print("Error")
			print(e)
			traceback.print_exc()
			lidar.disconnect()
			running = False
			
