import time
import math

from controller import Controller
from direction import DirectionManager
from lidar import Lidar
from motors import MotorController

if __name__ == "__main__":

    controller = Controller()
    motors = MotorController()
    directions = DirectionManager()

    running = True
    while running:

        try:
            controller.update_button_states()

            if controller.button_states != []:
                x = controller.get_right_x_value()
                y = controller.get_right_y_value()
                x_l = controller.get_left_x_value()
                
                # center the coordinates..
                x -= 0.5
                y -= 0.5
                
                # flip the y axis so negative is down and positive is up
                y *= -1
                
                mag = math.sqrt(x**2 + y**2)
                
                # The greatest |mag| = 0.5. Map this to 100% duty cycle
                
                angle = math.atan2(y, x)

                power1 = math.sin(angle - (1/4)*math.pi)
                power2 = math.sin(angle + (1/4)*math.pi)
                turn = ((x_l / 255) - 0.5)
				
				
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

                print(f"Angle: {angle}")
                print(f"a_power: {a_power}") 
                print(f"b_power: {b_power}") 
                print(f"c_power: {c_power}")
                print(f"d_power: {d_power}") 
				
                motors.setMotorPower(motors.forwardA, motors.backwardA, motors.pwmA, a_power)
                motors.setMotorPower(motors.forwardB, motors.backwardB, motors.pwmB, b_power)
                motors.setMotorPower(motors.forwardC, motors.backwardC, motors.pwmC, c_power)
                motors.setMotorPower(motors.forwardD, motors.backwardD, motors.pwmD, d_power)
        
        except KeyboardInterrupt:
            print("Exiting for keyboard interrupt...")
            motors.cleanup()
            running = False
        
        except: 
            motors.cleanup()
            running = False
