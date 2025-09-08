from strategies.strategy_interface import StrategyInterface
from models.driver import Driver
from models.ride_request import RideRequest
from typing import List, Optional


MAX_POSSIBLE_RATING_DIFFERENCE = 5.0


class WeightedRatingStrategy(StrategyInterface):
    """
    Driver selection strategy that balances distance and rating compatibility.
    """
    
    def __init__(self, distance_weight: float = 0.6, rating_weight: float = 0.4):
        """
        Initialize the strategy with weights for distance vs rating matching.
        
        Args:
            distance_weight (float): How much to prioritize distance (0.0 to 1.0)
            rating_weight (float): How much to prioritize rating matching (0.0 to 1.0)
        """
        self.distance_weight = distance_weight
        self.rating_weight = rating_weight
    
    def get_best_driver(self, ride_request: RideRequest, drivers: List[Driver]) -> Optional[Driver]:
        """
        Find the best driver by balancing distance and rating compatibility.
        
        Args:
            ride_request (RideRequest): The ride request to match
            drivers (List[Driver]): Available drivers to choose from
            
        Returns:
            Optional[Driver]: Best matching driver, or None if no eligible drivers
        """
        eligible_drivers = self._get_eligible_drivers(ride_request, drivers)
        
        if not eligible_drivers:
            return None
        
        best_driver = None
        best_score = float('inf')
        
        for driver in eligible_drivers:
            score = self._calculate_driver_score(ride_request, driver)
            
            if score < best_score:
                best_score = score
                best_driver = driver
        
        return best_driver
    
    def _get_eligible_drivers(self, ride_request: RideRequest, drivers: List[Driver]) -> List[Driver]:
        """
        Filter drivers to only those who are available and can serve the requested vehicle type.
        
        Args:
            ride_request (RideRequest): The ride request
            drivers (List[Driver]): All available drivers
            
        Returns:
            List[Driver]: Filtered list of eligible drivers
        """
        return [
            driver for driver in drivers
            if driver.is_available() and driver.can_serve_vehicle_type(ride_request.requested_vehicle_type)
        ]

    
    def _calculate_driver_score(self, ride_request: RideRequest, driver: Driver) -> float:
        """
        Calculate the combined weighted score for a driver.
        
        Args:
            ride_request (RideRequest): The ride request
            driver (Driver): The driver to score
            
        Returns:
            float: Combined score (lower is better)
        """
        distance_score = self._calculate_distance_score(ride_request, driver)
        rating_score = self._calculate_rating_score(ride_request, driver)
        
        return (self.distance_weight * distance_score) + (self.rating_weight * rating_score)
    
    def _calculate_distance_score(self, ride_request: RideRequest, driver: Driver) -> float:
        """
        Calculate the distance score for a driver (0-1, lower is better).
        
        Args:
            ride_request (RideRequest): The ride request
            driver (Driver): The driver to score
            
        Returns:
            float: Distance score between 0 and 1
        """
        distance_km = driver.location.calculate_distance_in_kilometer(ride_request.pickup_location)
        return distance_km / (distance_km + 1.0)  # Always between 0 and 1
    
    def _calculate_rating_score(self, ride_request: RideRequest, driver: Driver) -> float:
        """
        Calculate the rating compatibility score (0-1, lower is better).
        
        Args:
            ride_request (RideRequest): The ride request
            driver (Driver): The driver to score
            
        Returns:
            float: Rating compatibility score between 0 and 1
        """
        rating_diff = abs(ride_request.user_rating - driver.rating)
        return rating_diff / MAX_POSSIBLE_RATING_DIFFERENCE  # Normalize by max possible difference
