import hid

class Controller:

    def __init__(self):
        
        self.connected = False
        self.gamepad = None
        self.button_states = None
        self.toggleFlag = 0 

        self.connect()

    def connect(self):
        """ Method to connect to the DS4 PS4 controller """
        
        while not self.connected:
            try:
                self.gamepad = hid.Device(0x054c, 0x09cc)
                self.connected = True
            except:
                print("Failed to connect to controller...")
                print("Retrying...")

    def update_button_states(self): 
        self.button_states = list(self.gamepad.read(64))

    def get_right_x_value(self):
        return self.button_states[5]
    
    def get_right_y_value(self):
        return self.button_states[6]
    
    def get_left_x_value(self):
        return self.button_states[3]
    
    def get_circle_button(self):
        circleDetect = self.button_states[5]        
        return circleDetect & 64 == 64  
