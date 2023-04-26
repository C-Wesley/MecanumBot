from lidar import Lidar
import time 

if __name__ == "__main__":
	
	myLidar = Lidar()
	
	numScans = int(input("Enter a number of scans"))
	
	start = time.time()
	scans = myLidar.scan(numScans)
	elapsed = time.time() - start
	
	print(f"Eaplsed time for scanning: {elapsed}") 
	
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
	# for key, value in myScans.items():
		
		# print(f" Angle: {key} Dis: {value}")
