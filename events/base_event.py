from .enums import EventType


class BaseEvent:
    def __init__(self, timestamp: float):
        self.timestamp = timestamp