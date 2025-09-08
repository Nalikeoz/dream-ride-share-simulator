from dataclasses import dataclass
from typing import Optional
from .location import Location
from .enums import VehicleType, DriverStatus


@dataclass
class Driver:
    id: str
    name: str
    vehicle_type: VehicleType
    location: Location
    rating: float
    status: DriverStatus = DriverStatus.AVAILABLE
    current_ride_id: Optional[str] = None
    busy_until_timestamp: Optional[float] = None
    
    def is_available(self) -> bool:
        """
        Check if the driver is available for new rides.
        
        Returns:
            bool: True if driver is available, False otherwise
        """
        return self.status == DriverStatus.AVAILABLE
    
    def can_serve_vehicle_type(self, requested_vehicle_type: VehicleType) -> bool:
        """
        Check if the driver can serve a specific vehicle type request.
        
        Args:
            requested_vehicle_type (VehicleType): The requested vehicle type
            
        Returns:
            bool: True if driver can serve this vehicle type, False otherwise
        """
        return self.vehicle_type == requested_vehicle_type
    
    def assign_ride(self, ride_id: str, completion_time: float) -> None:
        """
        Assign a ride to this driver.
        
        Args:
            ride_id (str): ID of the ride being assigned
            completion_time (float): Timestamp when the ride will be completed
        """
        if not self.is_available():
            raise ValueError(f"Driver {self.id} is not available for assignment")
        
        self.current_ride_id = ride_id
        self.status = DriverStatus.BUSY
        self.busy_until_timestamp = completion_time
    
    def complete_ride(self) -> None:
        """
        Mark the current ride as completed and make the driver available again.
        """
        if self.is_available():
            raise ValueError(f"Driver {self.id} is not currently busy")
        
        self.status = DriverStatus.AVAILABLE
        self.current_ride_id = None
        self.busy_until_timestamp = None