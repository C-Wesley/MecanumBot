import time             # Time is used for timing
import RPi.GPIO as GPIO # GPIO is used to access GPIO pins
import math             # Math is math
import hid              # Hid is for controller
import sys              # sys is for system 

def setMotorDirection(fowardPin, backwardPin, isForwards):
	""" 
	Function to set the direction of motor a.
	forwardPin and backwardPin are the pins that control the direction of current. 
	Each motor has their own two.  
	isForwards is a bool and represents if the motor is going forwards. 
	"""
	
	GPIO.output(fowardPin, isForwards)
	GPIO.output(backwardPin, not isForwards)

def setEnablePins(aValue, bValue, cValue, dValue):
	"""
	Function that will set the enable values for all the motors
	"""
	
	GPIO.output(enable_a, aValue)
	GPIO.output(enable_b, bValue)
	GPIO.output(enable_c, cValue)
	GPIO.output(enable_d, dValue)

def goForward():
	"""
	Function that will set the motors in the proper state to go foward
	""" 
	
	setEnablePins(True, True, True, True)
	setMotorDirection(forwardA, backwardA, True)
	setMotorDirection(forwardB, backwardB, True)
	setMotorDirection(forwardC, backwardC, True)
	setMotorDirection(forwardD, backwardD, True)
	
def goBackward():
	"""
	Function that will set the motors in the proper state to go backward
	"""

	setEnablePins(True, True, True, True)
	setMotorDirection(forwardA, backwardA, False)
	setMotorDirection(forwardB, backwardB, False)
	setMotorDirection(forwardC, backwardC, False)
	setMotorDirection(forwardD, backwardD, False)
	

def main():
	
	delay = 2
	try:
		while True:
			
			#Test Going forward
			goForward()
			time.sleep(delay*2)
			
			#Test going backward
			goBackward()
			time.sleep(delay*2)
			
			#Reset all to false 
			setEnablePins(False, False, False, False)
			
			GPIO.output(enable_a, True)  # output is digitalWrite in arduino
			
			# Try same direction
			# one input pin should be high while the other low. 
			# This will change the direction that the motor. 
			print("First Motor Forward...")
			setMotorDirection(forwardA, backwardA, True)
			time.sleep(delay)           # Wait for one second
			
			
			# Try other direction
			print("First Motor Backward...")
			setMotorDirection(forwardA, backwardA, False)
			time.sleep(delay)
	
			GPIO.output(enable_a, False)
			
			# Try Other wheel 
			GPIO.output(enable_b, True)

			# Try same direction
			print("Second motor Forward...")
			setMotorDirection(forwardB, backwardB, True)
			time.sleep(delay)           # Wait for x seconds
			
			# Try other direction
			print("Second motor backward...")
			setMotorDirection(forwardB, backwardB, False)
			time.sleep(delay)
			
			GPIO.output(enable_b, False)
			
			GPIO.output(enable_c, True)
			
			print("Third motor forward...")
			setMotorDirection(forwardC, backwardC, True)
			time.sleep(delay)
			
			print("Third motor backward...")
			setMotorDirection(forwardC, backwardC, False)
			time.sleep(delay)
			
			GPIO.output(enable_c, False)

			GPIO.output(enable_d, True)
			
			print("Fourth motor forward...")
			setMotorDirection(forwardD, backwardD, True)
			time.sleep(delay)
			
			print("Fourth motor backward...")
			setMotorDirection(forwardD, backwardD, False)
			time.sleep(delay)
			
			GPIO.output(enable_d, False)

			
	except Exception as e:  # For most exceptions 
		print(e)
		GPIO.cleanup()
		
	except:                 # For keyboard interrupt
		GPIO.cleanup()

def testPwm():
	
	try:
		setMotorDirection(forwardA, backwardA, True)
		setMotorDirection(forwardB, backwardB, True)
		setMotorDirection(forwardC, backwardC, True)
		setMotorDirection(forwardD, backwardD, True)
		
		# range
		for x in range(10, 101, 10):
			print(f"Testing PWM of {x}.")
			pwmA.ChangeDutyCycle(x) # x percent
			pwmB.ChangeDutyCycle(x)
			pwmC.ChangeDutyCycle(x)
			pwmD.ChangeDutyCycle(x) 
			time.sleep(2)
		
		GPIO.cleanup()
	except:
		GPIO.cleanup()
	
def mock_joystick():
	# Mock joystick values for up still, right, left, up, down 
	dirs = ["still", "right", "left", "up", "down", "diag"]
	x = [512, 1023, 0, 512, 512, 768]
	y = [512, 512, 512, 1023, 0, 768]
	indx = 0
	for a,b in zip(x,y):

		# center the Coordinates to (0,0)
		new_x = a - 512
		new_y = b - 512
		
		print("----------")
		print(dirs[indx])
		indx+=1
		
		# Get the angle and magnitude from the joystick components
		angle = math.atan2(new_y, new_x)
		mag = math.sqrt(new_y**2 + new_x**2)
		
		print(f"Angle: {angle}, {angle*(180/math.pi)}")
		
		# Compute the speed for each motor
		power1 = math.sin(angle - (1/4 * math.pi)) * mag
		power2 = math.sin(angle + (1/4 * math.pi)) * mag
		
		# Rescale the speed to be from 0 - 100
		new_power1 = int((power1/(math.sqrt((256**2)<<1)) * 100))
		new_power2 = int( (power2/(math.sqrt((256**2)<<1)) * 100))
		
		print(f"Power1: {new_power1}") 
		print(f"Power2: {new_power2}") 
		
		# Set the direction for front left and back right motors
		if (new_power1 > 0):
			setMotorDirection(forwardA, backwardA, True)
			setMotorDirection(forwardC, backwardC, True)
		else:
			setMotorDirection(forwardA, backwardA, False)
			setMotorDirection(forwardC, backwardC, False)
		
		# Set the speed for front left and back right motors
		pwmA.ChangeDutyCycle(abs(new_power1)) # x percent
		pwmC.ChangeDutyCycle(abs(new_power1))
		
		# Set the direction for the front right and back left motors
		if (new_power2 > 0):
			setMotorDirection(forwardB, backwardB, True)
			setMotorDirection(forwardD, backwardD, True)
		else:
			setMotorDirection(forwardB, backwardB, False)
			setMotorDirection(forwardD, backwardD, False)
		
		# Set the speed for the front right and back left motors
		pwmB.ChangeDutyCycle(abs(new_power2)) # x percent
		pwmD.ChangeDutyCycle(abs(new_power2))
		
		# Delay 
		time.sleep(1)
			
	GPIO.cleanup()

def test_one_wheel(forwardPin, backwardPin, pwmObject):
	
	pwmObject.ChangeDutyCycle(100)
	
	setMotorDirection(forwardPin, backwardPin, True)
	time.sleep(5)
	
	setMotorDirection(forwardPin, backwardPin, False)
	time.sleep(5)

def no_wolves_map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def actual_joystick():
	
	while True:
		try:
			# Read data from the controller
			button_states = gamepad.read(64)
			if button_states:
				print("-----")
				right_x = button_states[3] - 128
				right_y = (button_states[4] - 128) * -1
				
				# Get the angle and magnitude from the joystick components
				angle = math.atan2(right_y, right_x)
				mag = math.sqrt(right_y**2 + right_x**2)
				
				print(f"Angle: {angle}, {angle*(180/math.pi)}")
				
				# Compute the speed for each motor
				power1 = math.sin(angle - (1/4 * math.pi)) * mag
				power2 = math.sin(angle + (1/4 * math.pi)) * mag
							
				# Rescale the speed to be from 0 - 100
				new_power1 = int(no_wolves_map(power1, -150, 150, -100, 100))
				new_power2 = int(no_wolves_map(power2, -150, 150, -100, 100))
				
				print(f"Power1: {new_power1}") 
				print(f"Power2: {new_power2}") 
				
				# Set the direction for front left and back right motors
				if (new_power2 > 0):
					setMotorDirection(forwardA, backwardA, True)
					setMotorDirection(forwardC, backwardC, True)
				else:
					setMotorDirection(forwardA, backwardA, False)
					setMotorDirection(forwardC, backwardC, False)
				
				# Set the speed for front left and back right motors
				pwmA.ChangeDutyCycle(abs(new_power2)) # x percent
				pwmC.ChangeDutyCycle(abs(new_power2))
				
				# Set the direction for the front right and back left motors
				if (new_power1 > 0):
					setMotorDirection(forwardB, backwardB, True)
					setMotorDirection(forwardD, backwardD, True)
				else:
					setMotorDirection(forwardB, backwardB, False)
					setMotorDirection(forwardD, backwardD, False)
				
				# Set the speed for the front right and back left motors
				pwmB.ChangeDutyCycle(abs(new_power1)) # x percent
				pwmD.ChangeDutyCycle(abs(new_power1))
				
			else:
				print("----")
				print("No states ready...")
		except:
			GPIO.cleanup()
	
	
	
	
if __name__ == "__main__":
	
	# Try to init controller...
	try:
		gamepad = hid.device()
		gamepad.open(0x054c, 0x09cc)
		gamepad.set_nonblocking(True)
	except Exception as e:
		print(e)
		print("Could not open controller... :(")
		sys.exit(1)
	
	### Begin Setup ### 
	# Set up the motor controller pins
	# Set up the motor controller pins for the front motors
	
	enable_a  = 21 # Front left motor
	enable_b  = 4  # Ront Right motor
	forwardA  = 16
	backwardA = 20
	forwardB  = 17
	backwardB = 27
	enable_c  = 24 # Back Right Motor
	enable_d  = 13 # Back Left Motor
	forwardC  = 23
	backwardC = 18
	forwardD  = 26
	backwardD = 19

	# Use the BCM pinout
	GPIO.setmode(GPIO.BCM)
	
	GPIO.setup(enable_a, GPIO.OUT) # setup is pinMode in arduino
	GPIO.setup(enable_b, GPIO.OUT)
	GPIO.setup(forwardA, GPIO.OUT)
	GPIO.setup(backwardA, GPIO.OUT)
	GPIO.setup(forwardB, GPIO.OUT)
	GPIO.setup(backwardB, GPIO.OUT)
	GPIO.setup(enable_c, GPIO.OUT)
	GPIO.setup(enable_d, GPIO.OUT)
	GPIO.setup(forwardC, GPIO.OUT)
	GPIO.setup(backwardC, GPIO.OUT)
	GPIO.setup(forwardD, GPIO.OUT)
	GPIO.setup(backwardD, GPIO.OUT)
	
	# Create PWM objects
	# PWM_Object = GPIO.PWM(pin#, frequency)
	pwmA = GPIO.PWM(enable_a, 100)  
	pwmB = GPIO.PWM(enable_b, 100) 
	pwmC = GPIO.PWM(enable_c, 100)
	pwmD = GPIO.PWM(enable_d, 100)
	
	# PWM_object.start(dutyCycle) 
	pwmA.start(0)
	pwmB.start(0)
	pwmC.start(0)
	pwmD.start(0)

	# Turn off all the motors
	GPIO.output(enable_a, False)
	GPIO.output(enable_b, False)
	GPIO.output(enable_c, False)
	GPIO.output(enable_d, False)
	
	actual_joystick()
	#mock_joystick()
	#testPwm()
	
	GPIO.cleanup()
	#main()
	
	
