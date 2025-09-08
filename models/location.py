import math
from dataclasses import dataclass
from geopy.distance import geodesic


@dataclass
class Location:
    latitude: float
    longitude: float
    
    def calculate_distance_in_kilometer(self, other_location: 'Location') -> float:
        """
        Calculate the distance between two locations in kilometers.
        
        Args:
            other_location (Location): The other location to calculate the distance to
            
        Returns:
            float: The distance in kilometers
        """
        distance_object = geodesic(
            (self.latitude, self.longitude),
            (other_location.latitude, other_location.longitude)
        )
        
        distance_in_kilometers = distance_object.kilometers
        return distance_in_kilometers