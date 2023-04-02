import cv2 

# first parameter is the index and the second one is for V4L2 enables cap via libv4l 
cam = cv2.VideoCapture(0, cv2.CAP_V4L2) 			

try: 
	# names the window
	cv2.namedWindow("test") 	
	
	# Infinite Loop. Like loop() in arduino					
	while True:
		# cam.read() returns 2 values, ret = 0,1 and img is actual image object 									
		ret, img = cam.read() 	
		
		# if we got an image back		
		if ret: 
			 # show the image on window named "test"
			cv2.imshow("test", img)
			# waiting for user input for 1 ms, if it doesnt get input then continue
			cv2.waitKey(1) 
		
except Exception as e:
	# print error message
	print(e) 
	# free the camera object from memory
	cam.release() 
	# delete all windows made
	cam.destroyAllWindows() 
