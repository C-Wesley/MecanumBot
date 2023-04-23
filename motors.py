import RPi.GPIO as GPIO

class MotorController:
    
    def __init__(self):

        self.enable_a  = 21 # Front left motor
        self.enable_b  = 4  # Ront Right motor
        self.forwardA  = 16
        self.backwardA = 20
        self.forwardB  = 17
        self.backwardB = 27
        self.enable_c  = 24 # Back Right Motor
        self.enable_d  = 13 # Back Left Motor
        self.forwardC  = 23
        self.backwardC = 18
        self.forwardD  = 26
        self.backwardD = 19

        # Use the BCM pinout
        GPIO.setmode(GPIO.BCM)
        
        # setup is pinMode in arduino
        GPIO.setup(self.enable_a, GPIO.OUT) 
        GPIO.setup(self.enable_b, GPIO.OUT)
        GPIO.setup(self.forwardA, GPIO.OUT)
        GPIO.setup(self.backwardA, GPIO.OUT)
        GPIO.setup(self.forwardB, GPIO.OUT)
        GPIO.setup(self.backwardB, GPIO.OUT)
        GPIO.setup(self.enable_c, GPIO.OUT)
        GPIO.setup(self.enable_d, GPIO.OUT)
        GPIO.setup(self.forwardC, GPIO.OUT)
        GPIO.setup(self.backwardC, GPIO.OUT)
        GPIO.setup(self.forwardD, GPIO.OUT)
        GPIO.setup(self.backwardD, GPIO.OUT)

        # Create PWM objects
	    # PWM_Object = GPIO.PWM(pin#, frequency)
        self.pwmA = GPIO.PWM(self.enable_a, 100)  
        self.pwmB = GPIO.PWM(self.enable_b, 100) 
        self.pwmC = GPIO.PWM(self.enable_c, 100)
        self.pwmD = GPIO.PWM(self.enable_d, 100)

        self.pwmA.start(0)
        self.pwmB.start(0)
        self.pwmC.start(0)
        self.pwmD.start(0)

        # Turn off all the motors
        GPIO.output(self.enable_a, False)
        GPIO.output(self.enable_b, False)
        GPIO.output(self.enable_c, False)
        GPIO.output(self.enable_d, False)
    
    def setMotorDirectionBool(self, forwardPin, backwardPin, isForwards):
        """ 
        Method to set the direction of a motor based on a bool
        
        forwardPin, backwardPin => the output pins of the motor controller. 

        isForward :bool: Set the motor set to forwards?   
        """

        GPIO.output(forwardPin, isForwards)
        GPIO.output(backwardPin, not isForwards)
    
    def setMotorPower(self, forwardPin, backwardPin, enableObject, power):
        """
        Method to set the direction of a motor based on it's power

        forwardPin, backwardPin => the output pins of the motor controller.
        enablePin 

        power :float: the power to set the motor to 
        """

        # Make sure the direction is consistent for the power
        if power > 0:
            self.setMotorDirectionBool(forwardPin, backwardPin, True)
        else:
            self.setMotorDirectionBool(forwardPin, backwardPin, False)
        
        enableObject.ChangeDutyCycle(abs(power))
    
    def cleanup(self):
        GPIO.cleanup()

    def stopAllMotors(self):
        """
        Method to stop all the motors
        """
        
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        self.pwmC.ChangeDutyCycle(0)
        self.pwmD.ChangeDutyCycle(0)
