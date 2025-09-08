from dataclasses import dataclass

from .location import Location
from .enums import VehicleType


@dataclass
class RideRequest:
    id: str
    pickup_location: Location
    dropoff_location: Location
    requested_vehicle_type: VehicleType
    timestamp: float
    user_rating: float