from .base_event import BaseEvent
from models.ride_request import RideRequest


class RideRequestEvent(BaseEvent):
    def __init__(self, ride_request_timestamp: float, ride_request: RideRequest):
        super().__init__(ride_request_timestamp)
        self.ride_request = ride_request