import hid
import sys
import time

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
		
		# Print out the report to view
		for indx, byte in enumerate(report[3:8]):
			print(f"byte[{indx+3}] = {byte}, {hex(byte)}, ", end="")
			print("{:08b}".format(byte))
		
		
except Exception as e:
	print(e)
except KeyboardInterrupt:
	print("Exiting gracefully...")
	sys.exit(0)
