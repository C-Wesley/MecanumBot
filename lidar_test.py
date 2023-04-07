# Following a guide from: 
# https://learn.adafruit.com/slamtec-rplidar-on-pi/cpython-on-raspberry-pi

from adafruit_rplidar import RPLidar
import matplotlib.pyplot as plt
import math
import time
import sys
import numpy

# Function defintions 

def process_data_scans(scans):
	
	# Create a list for angles and distances
	angles, distances = [], []
	
	for scan in scans:
		# in each scan we can look at the quality, the angle, and the distance
		for _, angle, dis in scan:
			# Take the angle and append it to a list in radian format
			angles.append(angle*(math.pi/180))
			# Take the distance and append it to a list
			distances.append(dis)
	
	# Clear our axis 
	ax.clear()
	# Limit it to 500 (found expirementally for the desk)
	ax.set_rlim([0, 500])
	# Plot the radians and distances
	ax.scatter(angles, distances, s=5)
	# Update the figure
	fig.canvas.draw()
	fig.canvas.flush_events()
	time.sleep(.1)


def connect_to_lidar():
	
	# Until the lidar is connected
	while True:
		
		try:
			print("Trying to connect to lidar...")
			
			# Try to connect to the port
			PORT_NAME = '/dev/ttyUSB0'
			lidar = RPLidar(None, PORT_NAME, timeout=3)
			break
		except Exception as e:
			print(e)
		except:
			print("Something failied...")
			print("Trying again in 5 seconds")
			time.sleep(5)
	
	# If we made it here, return the lidar object
	return lidar


|## Main body of code ## 

# Create an interactive matplotlib plot. 
plt.ion()
fig = plt.figure() 
ax = fig.add_subplot(projection='polar') # Set it to polar 

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

		process_data_scans(scans)

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
