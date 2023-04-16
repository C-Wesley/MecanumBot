import time             # Time is used for timing
import RPi.GPIO as GPIO # GPIO is used to access GPIO pins
import math             # Math is math
import hid              # Hid is for controller
import sys              # sys is for system 
from lidar_test import connect_to_lidar

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
			button_states = list(gamepad.read(64))
			if button_states:
				print("-----")
				# Normalize the coordinates. This puts then in the range [0, 1]
				x = button_states[5] / 255 
				y = button_states[6] / 255 
				
				# center the coordinates..
				x -= 0.5
				y -= 0.5
				
				# flip the y axis so negative is down and positive is up
				y *= -1
				
				mag = math.sqrt(x**2 + y**2)
				
				# The greatest |mag| = 0.5. Map this to 100% duty cycle
				
				angle = math.atan2(y, x)
				
				"""
				power1 = math.sin(angle - (1/4 * math.pi)) * mag 
				power2 = math.sin(angle + (1/4 * math.pi)) * mag 
				"""
				
				power1 = math.sin(angle - (1/4)*math.pi)
				power2 = math.sin(angle + (1/4)*math.pi)
				turn = ((button_states[3] / 255) - 0.5)
				
				
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
 
				"""
				a_power = 100 * (power2 + turn) 
				c_power = 100 * (power2 - turn) 
				b_power = 100 * (power1 - turn) 
				d_power = 100 * (power1 + turn) 
				"""
				print(f"Angle: {angle}")
				print(f"a_power: {a_power}") 
				print(f"b_power: {b_power}") 
				print(f"c_power: {c_power}")
				print(f"d_power: {d_power}") 
				
				set_direction(forwardA, backwardA, a_power)
				set_direction(forwardB, backwardB, b_power)
				set_direction(forwardC, backwardC, c_power)
				set_direction(forwardD, backwardD, d_power)
				
				pwmA.ChangeDutyCycle(abs(a_power))
				pwmB.ChangeDutyCycle(abs(b_power))
				pwmC.ChangeDutyCycle(abs(c_power))
				pwmD.ChangeDutyCycle(abs(d_power))
				
			
				
				print(turn)
				"""
				if (x_left > 0.2):
					# Invert FL and BR, and FR and BL 
					setMotorDirection(forwardA, backwardA, True)
					setMotorDirection(forwardC, backwardC, False)
					setMotorDirection(forwardB, backwardB, False)
					setMotorDirection(forwardD, backwardD, True)
				elif (x_left < -0.2):
					setMotorDirection(forwardA, backwardA, False)
					setMotorDirection(forwardC, backwardC, True)
					setMotorDirection(forwardB, backwardB, True)
					setMotorDirection(forwardD, backwardD, False) """
				
			else:
				print("----")
				print("No states ready...")
		except Exception as e:
			print(e)
		except:
			GPIO.cleanup()
			break

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
    
def set_direction(forwardsPin, backwardsPin, power):
	
	if power > 0:
		setMotorDirection(forwardsPin, backwardsPin, True)
	else:
		setMotorDirection(forwardsPin, backwardsPin, False)
	
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

def autonomous_movement():

	while True:
		
		# Make sure we are stationary 
		pwmA.ChangeDutyCycle(0)
		pwmB.ChangeDutyCycle(0)
		pwmC.ChangeDutyCycle(0)
		pwmD.ChangeDutyCycle(0)

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

			angle = process_scans(scans)

			mag = 0.5
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

			# let it travel for 2 seconds
			time.sleep(2)

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





	mag = 0.5
    #may need some delays

	angle = process_scans()

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








if __name__ == "__main__":
	
	# Try to init controller...
	try:
		gamepad = hid.Device(0x054c, 0x09cc)
		#gamepad.open()
		#gamepad.set_nonblocking(True)
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
	
	#actual_joystick()
	#mock_joystick()
	#testPwm()
	
	GPIO.cleanup()
	#main()
	
	
