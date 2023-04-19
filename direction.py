import math 

class DirectionManager:

    def __init__(self, lowerBound, upperBound, distance_thresh):
        """
        Constructor for our DirectionManager object.

        lowerBound :radians: The lower bound of the angles to view
        upperBound :radians: The upper bound of the angles to view
        distance_threshold :mm: How close is too close?
        """
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.disThres = distance_thresh

        self.filteredScans = {}
    
    def filter_scans(self, scans):
        """
        Filter the scans based on the lower and upper bound
        """
        
        # Dictionary for our distances and angles
        self.filteredScans = {}

        for scan in scans:

            for _, angle, dis in scan:

                angle = 2*math.pi - (angle*math.pi/180)

                if (angle >= self.lowerBound and angle <= self.upperBound):
                    self.filteredScans[angle] = dis
        
    def get_angle_wth_max_distance(self):
        """ Gets the angle that has the max distance from the filtered scans """

        return max(self.filteredScans, key=self.filteredScans.get)   
    
    def get_min_distance(self):
        """ Gets the min distance from the filtered scans """

        return min(self.filteredScans.values())