#from lidar import Lidar
import time 
from adafruit_rplidar import RPLidar
from lidar import Lidar

def method_one():
	PORT_NAME = '/dev/ttyUSB0'
	lidar = RPLidar(None, PORT_NAME, timeout=3)
	
	numScans = int(input("Enter a number of scans"))
	
	scans = []
	
	while True:
		time.sleep(0.1)
		start = time.time()
		#lidar.reset()
		lidar.clear_input()
		lidar.connect()

		for indx, scan in enumerate(lidar.iter_scans()):
			if indx > numScans:
				lidar.stop()
				break
			else:
				scans.append(scan)
		elapsed = time.time() - start
		print(f"Elapsed Time {elapsed}.")
	
		myScans = {}
		start = time.time()
		for scan in scans:
			for _, angle, dis in scan:
				myScans[angle] = dis
		elapsed = time.time() - start
		
		print("# Angles: ", end="")
		print(len(myScans.keys()))
	
		print(f"Time: {elapsed}") 
		print()
	


if __name__ == "__main__":
	

	method_one()
	# print("# Angles: ", end="")
	# print(len(myScans.keys()))
	
	# print(f"Time: {elapsed}") 
				
	# print(f"Eaplsed time for scanning: {elapsed}") 
	
	# myScans = {}
	
	# start = time.time()
	# for scan in scans:
		# for _, angle, dis in scan:
			# myScans[angle] = dis
	# elapsed = time.time() - start
	
	
	# print("# Angles: ", end="")
	# print(len(myScans.keys()))
	
	# print(f"Time: {elapsed}") 
	
	# print()
	# # for key, value in myScans.items():
		
		# # print(f" Angle: {key} Dis: {value}")
