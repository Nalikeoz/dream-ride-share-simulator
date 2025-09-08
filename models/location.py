import math
from dataclasses import dataclass


@dataclass
class Location:
    latitude: float
    longitude: float
    
    def calculate_distance(self, other_location: 'Location') -> float:
        driver_to_pickup_distance = math.dist(
            (self.latitude, self.longitude), 
            (other_location.latitude, other_location.longitude)
        )
        return driver_to_pickup_distance