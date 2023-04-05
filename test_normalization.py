import hid
import sys
import time
import math

# Hardcoded device for the Sony Dual Shock 4
vendorId = 1356
productId = 2508

# Print out all the HID devices
for indx, device in enumerate(hid.enumerate()):
	print("-"*20, f"\nDevice{indx}\n", device, "\n", "-"*20, "\n")

try:
	# Try to open the device 
	gamepad = hid.Device(vendorId, productId)
except Exception as e:
	print()
	print("Could not open the hard coded device...")
	print(e)
	print()
	sys.exit(1)

# If we made it this far, the device opened
print("Device opened!")

try:
	while True:
		
		#Get the report 
		report = list(gamepad.read(78))
		
		# Normalize the coordinates. This puts then in the range [0, 1]
		x = report[5] / 255 
		y = report[6] / 255 
		
		# center the coordinates..
		x -= 0.5
		y -= 0.5
		
		# flip the y axis so negative is down and positive is up
		y *= -1
		
		mag = math.sqrt(x**2 + y**2)
		
		# The greatest |mag| = 0.5. Map this to 100% duty cycle
		
		
		angle = math.atan2(y, x)
		power1 = math.sin(angle - (1/4 * math.pi)) * mag
		power2 = math.sin(angle + (1/4 * math.pi)) * mag
		

		
		x_left = ((report[3] / 255) - 0.5) * 2
		
		power1 += x_left
		power2 += x_left
		
			
		power1 *= 100
		power2 *= 100
		
		print(x, ",", y, ",", power1, ",", power2)
		
		
		
except Exception as e:
	print(e)
except KeyboardInterrupt:
	print("Exiting gracefully...")
	sys.exit(0)
