from .base_event import BaseEvent
from models.driver import Driver

class RideCompletionEvent(BaseEvent):
    def __init__(self, ride_completion_timestamp: float, ride_id: str, driver: Driver):
        super().__init__(ride_completion_timestamp)
        self.ride_id = ride_id
        self.driver = driver