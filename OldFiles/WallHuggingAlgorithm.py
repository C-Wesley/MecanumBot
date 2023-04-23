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
	turn = 0
    
	
	running = True
	while running:
		try:
			# make sure we are stationary 
			motors.stopAllMotors()
			
			# Get some scans
			scans = lidar.scan(num_scans)

			# Process the scans 
			directions.filter_scansAlg(scans)
			
			# Get the variables we need to make decisions with 
			upperDistance = directions.filteredScansAngle[directions.upperBound]
			lowerDistance = directions.filteredScansAngle[directions.lowerBound]
			
			mag = 0.5

            # Include turn
			

			if(upperDistance > lowerDistance):
				turn = (upperDistance - lowerDistance/max(upperDistance+lowerDistance))
			elif(upperDistance < lowerDistance):
				turn = (lowerDistance - upperDistance/max(upperDistance+lowerDistance))
                

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

			print(f"Angle: {angle}")
			print(f"a_power: {a_power}") 
			print(f"b_power: {b_power}") 
			print(f"c_power: {c_power}")
			print(f"d_power: {d_power}") 
				
			motors.setMotorPower(motors.forwardA, motors.backwardA, motors.pwmA, a_power)
			motors.setMotorPower(motors.forwardB, motors.backwardB, motors.pwmB, b_power)
			motors.setMotorPower(motors.forwardC, motors.backwardC, motors.pwmC, c_power)
			motors.setMotorPower(motors.forwardD, motors.backwardD, motors.pwmD, d_power)
			
			time.sleep(1)
		
	
		except KeyboardInterrupt:
			print("Exiting for keyboard interrupt")
			motors.cleanup()
			lidar.disconnect()
			running = False
		
		except Exception as e:
			print(e)
			lidar.disconnect()
			
			
