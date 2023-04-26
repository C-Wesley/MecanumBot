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
	num_scans = 10
	turn = 0

	running = True
	while running:
		try:
			# make sure we are stationary
			#motors.stopAllMotors()
			
			# Get some scans
			scans = lidar.scan(num_scans)

			# Process the scans 
			directions.filter_scansAlg180(scans)
			# Get the variables we need to make decisions with 
			print(directions.filteredScansAngle)
			
			x2 = 800 #upper Bound
			x1 = 300 #lower Bound
			wall = directions.filteredScansAngle.get(int(math.pi), 0) #gets the distance at angle 180
			lower = directions.filteredScansAngle.get(int(directions.lowerBound*(180/math.pi)), 0) #gets the distance at angle 150
			upper = directions.filteredScansAngle.get(int(directions.upperBound*(180/math.pi)), 0) 
			

			if wall != 0 and lower != 0 and upper != 0:
				
				print(wall)
				mag = 0.20

				#Include turn
				if wall > x1 and wall < x2: #if the car is between both distance we do minor turns
					
					angle = math.pi/2 #set the angle to 90
					#if currentDistance > (x2 - x1)/2:
						#turn left
					#	turn = 0.03
					#elif currentDistance < (x2 - x1)/2:
						#turn right
					#	turn = -0.03
					#else:
					#	turn = 0
					
						
				elif wall > x2:	#if the car is passed x2 the car moves left to get back into the center			
					angle = math.pi/2 + math.atan2(math.sqrt(lower**2+wall**2), wall)				
				elif wall < x1: #if the car is passed x1 the car moves right to get back into the center		
					angle = math.pi/2 - math.atan2(math.sqrt(lower**2+wall**2), wall)	
				else:
					turn = 0
				
				turn = (upper-lower)/max(upper, lower)
				turn = turn/4

#everything is kept the same here
				print(f"Turn: {turn}")
				print(f"Angle: {angle*180/math.pi}")
				power1 = (math.sin((angle)-(1/4)*math.pi))
				power2 = (math.sin((angle)+(1/4)*math.pi)) 
				
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
