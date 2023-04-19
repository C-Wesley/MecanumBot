from adafruit_rplidar import RPLidar

# Create a lidar class to manage our lidar connection
class Lidar: 

    def __init__(self):
        # The method is ran ever time an object 
        # is created 
        self.connected = False 
        self.lidar = None

    def connect(self):
        """
        Method to connect to the lidar
        using the RPLidar object
        """
        
        # Loop until we are connected 
        while not self.connected:
            
            # Not sure what errors we might encounter... 
            # So we use a try except 
            try:
                
                # Connect to this port 
                PORT_NAME = '/dev/ttyUSB0'
                lidar = RPLidar(None, PORT_NAME, timeout=3)
                
                # Set the flag for connection 
                # This will end the loop 
                self.connected = True

            except Exception as e:
                # If we encounter some error, print it.
                # The loop will continue 
                print("Failed to connect to lidar...")
                print("Retrying...")

        self.lidar = lidar
    
    def disconnect(self):
        """
        This method will disconnect from the lidar
        """

        self.lidar.stop()
        self.lidar.disconnect()
        self.connected = False
    
    def scan(self, num_scans):
        """
        This method will actually use the RPLidar object
        to gather some data from the scans
        """

        # If we are not connected, we need to connect. 
        if not self.connected:
            self.connect()
        else:
            # If we were previously connected, we should
            # disconnect and reconnect.
            self.disconnect()
            self.connect()
        
        scans = []
        # Try to gather some scans
        try:
            
            # for every scan, append it to a list
            for indx, scan in enumerate(self.lidar.iter_scans()):
                scans.append(scan)

                # If we have "num_scans" number of samples, we can continue
                if indx > num_scans:
                    break
            
            # Discconect from the lidar and return the scans
            self.disconnect()
            return scans
        
        except:
            
            print("Lidar scan failed")
            self.disconnect()
