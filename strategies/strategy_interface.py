from abc import ABC, abstractmethod
from typing import List
from models.driver import Driver
from models.ride_request import RideRequest


class StrategyInterface(ABC):
    @abstractmethod
    def get_best_driver(self, ride_request: RideRequest, drivers: List[Driver]) -> Driver:
        """
        Get the best driver for a given ride request according
        to a specific strategy.
        
        Args:
            ride_request (RideRequest): The ride request to get the best driver for
            drivers (List[Driver]): The list of drivers to choose from
            
        Returns:
            Driver: The best driver for the given ride request according to the strategy
        """
        pass