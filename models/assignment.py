from dataclasses import dataclass


@dataclass
class Assignment:
    timestamp: float
    ride_id: str
    driver_id: str
    pickup_eta_minutes: float