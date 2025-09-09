from strategies.strategy_interface import StrategyInterface
from models.driver import Driver
from models.ride_request import RideRequest



class StraightLineStrategy(StrategyInterface):
    def get_best_driver(self, ride_request: RideRequest, drivers: list[Driver]) -> Driver | None:
        """
        Find the available driver with the minimum distance to the pickup location.
        
        Returns:
            Driver | None: The driver with minimum distance, or None if no available drivers
        """
        # Filter available drivers who can serve the requested vehicle type
        eligible_drivers = [
            driver for driver in drivers
            if driver.is_available() and driver.can_serve_vehicle_type(ride_request.requested_vehicle_type)
        ]
        
        if not eligible_drivers:
            return None
        
        # Find driver with minimum distance
        best_driver = None
        min_distance = float('inf')
        
        for driver in eligible_drivers:
            distance = driver.location.calculate_distance_in_kilometer(ride_request.pickup_location)
            
            if distance < min_distance:
                min_distance = distance
                best_driver = driver
        
        return best_driver
    