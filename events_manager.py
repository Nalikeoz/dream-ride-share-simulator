from events.ride_request_event import RideRequestEvent
from events.ride_completion_event import RideCompletionEvent
from events.base_event import BaseEvent
from enum import Enum
from bisect import bisect_right


class EventPriority(Enum):
    HIGH = 0    # Highest priority (e.g., ride completions)
    MEDIUM = 1  # Medium priority (e.g., ride requests)
    LOW = 2     # Lowest priority (default for unknown event types)


class EventsManager:
    """
    Manages a priority queue of events for discrete event simulation.
    
    The EventsManager maintains a chronologically ordered list of events
    that need to be processed during the simulation. Events are sorted by:
    1. Timestamp (earliest first)
    2. Priority (higher priority first for same timestamp)
    3. Tie-breaking key (deterministic ordering for identical events)
    
    This implementation uses a sorted list with binary search insertion
    for efficient event scheduling while maintaining chronological order.
    
    Attributes:
        events (list): List of events in chronological order
        _keys (list): Parallel list of sort keys for efficient insertion
    """
    def __init__(self):
        self.events = []
        # self._keys is a parallel list to self.events to keep track of events order
        # and to lower time complexity for insertion
        self._keys = []
        
    def _get_event_priority(self, event: BaseEvent) -> EventPriority:
        """
        Determine the priority of an event based on its type.
        
        Args:
            event (BaseEvent): The event to determine priority for
            
        Returns:
            EventPriority: The priority level for this event type
            
        Note:
            RideCompletionEvent has HIGH priority (must be processed first)
            RideRequestEvent has MEDIUM priority
            Unknown event types default to LOW priority
        """
        _EVENT_PRIORITY_MAP = {
            RideCompletionEvent: EventPriority.HIGH,
            RideRequestEvent: EventPriority.MEDIUM
        }
        
        event_class = event.__class__
        if event_class in _EVENT_PRIORITY_MAP:
            return _EVENT_PRIORITY_MAP[event_class]
        
        return EventPriority.LOW
    
    def _get_tie_key(self, event: BaseEvent):
        if isinstance(event, RideCompletionEvent):
            return str(event.driver.id)
        
        if isinstance(event, RideRequestEvent):
            return str(event.ride_request.id)
        
        return ""
    
    def _get_sort_key(self, event: BaseEvent):
        return (
            event.timestamp, 
            self._get_event_priority(event), 
            self._get_tie_key(event)
        )

    def add_event(self, event: BaseEvent) -> None:
        """
        Adds an event to the event queue in the correct chronological position.
        
        Uses binary search to find the correct insertion point, maintaining
        the chronological order of events. The event is inserted based on
        its timestamp, priority, and tie-breaking key.
        
        Args:
            event (BaseEvent): The event to add to the queue
        """
        event_sort_key = self._get_sort_key(event)
        insertion_index = bisect_right(self._keys, event_sort_key)
        
        self._keys.insert(insertion_index, event_sort_key)
        self.events.insert(insertion_index, event)

    def get_next_event_generator(self):
        """
        Generator that yields events in chronological order.
        
        Removes and yields the next event from the front of the queue.
        This method maintains the chronological order by always returning
        the earliest event first.
        
        Yields:
            BaseEvent: The next event to be processed
        """
        while self.events:
            self._keys.pop(0)
            yield self.events.pop(0)
