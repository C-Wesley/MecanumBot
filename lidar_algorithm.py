from adafruit_rplidar import RPLidar
import matplotlib.pyplot as plt
import math
import time
import sys
import numpy

from MotorTest import set_direction
from lidar_test import connect_to_lidar

def process_scans(scans):

    #to set the cone range for movement
    lowerBound = math.pi/4
    upperBound = 3*lowerBound

    #dict data structure to store angle as key and distance as value
    dict = {}

    #alg for storing angle and distance based on the 2 bounds, accounted for y axis inversion
    for scan in scans:
        for _, angle, dis in scan:
            if(angle >= 5*lowerBound and angle <= 7*lowerBound): 
                angle = 2*math.pi - angle        
                dict[angle] = dis
    return max(dict, key = dict.get) #returns the key with the maximum dict so it returns the angle

def autoMovement():
	mag = 0.5
	
    #may need some delays
	angle = process_scans

	power1 = 100 * (math.sin(angle - (1/4)*math.pi) * mag)
	power2 = 100 * (math.sin(angle + (1/4)*math.pi) * mag)
							
	set_direction(forwardA, backwardA, power2)
	set_direction(forwardB, backwardB, power1)
	set_direction(forwardC, backwardC, power2)
	set_direction(forwardD, backwardD, power1)
		
	pwmA.ChangeDutyCycle(abs(power2))
	pwmB.ChangeDutyCycle(abs(power1))
	pwmC.ChangeDutyCycle(abs(power2))
	pwmD.ChangeDutyCycle(abs(power1))
				
			
			
            
## main body of code ##
# Until we exit the program
while True:
	
	# Get the lidar object
	lidar = connect_to_lidar()
	scans = []
	
	try:
		# Get the scans from the API
		for indx, scan in enumerate(lidar.iter_scans()):
			scans.append(scan)
			# If we got 10 scans, break to update our plot
			if indx > 10: 
				break
	
		# Disconnect from the lidar. 
		# I had issues trying to use the same lidar instance over time.
		# so we will just re instantiate it each time we need it.
		lidar.stop()
		lidar.disconnect()

		process_scans(scans)

	except KeyboardInterrupt:
		print('Exiting for keyboard interrupt...') # good 
		lidar.stop()
		lidar.disconnect()
		sys.exit(0)

	except Exception as e:
		print('Exiting for error...') # bad
		print(e)                      # print error
		lidar.stop()
		lidar.disconnect()
		sys.exit(1)