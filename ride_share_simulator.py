from strategies.strategy_factory import StrategyFactory
from models.simulation_result import SimulationResult
from events_manager import EventsManager
from events.ride_request_event import RideRequestEvent
from events.ride_completion_event import RideCompletionEvent
from data_parser import RideSimulationDataParser
from models.assignment import Assignment
from consts import StrategyType


class RideShareSimulator:
    """
    Main simulation engine for the ride-sharing system.
    
    The RideShareSimulator orchestrates the entire simulation process by managing
    events, drivers, and ride requests. It uses a discrete event simulation approach
    where events are processed in chronological order to simulate the real-time
    operation of a ride-sharing platform.
    """
    def __init__(self, data_file_path: str, strategy_type: str = StrategyType.STRAIGHT, 
                 distance_weight: float = 0.6, rating_weight: float = 0.4):
        """
        Initialize the RideShareSimulator with data and strategy configuration.
        
        Args:
            data_file_path (str): Path to the JSON file containing drivers and ride requests
            strategy_type (str): Type of strategy to use ('straight' or 'weighted')
            distance_weight (float): Weight for distance component (for weighted strategy)
            rating_weight (float): Weight for rating component (for weighted strategy)
        """
        self.simulation_result = SimulationResult()
        self.data_parser = RideSimulationDataParser(data_file_path)
        self._events_manager = EventsManager()
        self.drivers = self.data_parser.get_drivers()
        
        # Create strategy using factory
        self.strategy = StrategyFactory.create_strategy(
            strategy_type=strategy_type,
            distance_weight=distance_weight,
            rating_weight=rating_weight
        )
        
        self._schedule_events()
        
        self._EVENT_TYPE_TO_HANDLER = {
            RideRequestEvent: self._process_ride_request_event,
            RideCompletionEvent: self._process_ride_completion_event
        }
    
    
    def _schedule_events(self):
        """
        Schedule initial ride request events in the event queue.
        """
        for ride_request in self.data_parser.get_ride_requests():
            self._events_manager.add_event(RideRequestEvent(ride_request.timestamp, ride_request))
            
    def _process_ride_request_event(self, ride_request_event: RideRequestEvent):
        """
        Process a ride request event by finding the best driver and scheduling completion.
        
        Args:
            ride_request_event (RideRequestEvent): The ride request event to process
        """
        ride_request = ride_request_event.ride_request
        best_driver = self.strategy.get_best_driver(ride_request, self.drivers)
        
        if best_driver:
            # Calculate pickup ETA assuming average speed of 30 km/h
            pickup_eta_minutes = (best_driver.location.calculate_distance_in_kilometer(ride_request.pickup_location) / 30) * 60
            self.simulation_result.add_assignment(
                Assignment(
                    timestamp=ride_request.timestamp,
                    ride_id=ride_request.id,
                    driver_id=best_driver.id,
                    pickup_eta_minutes=pickup_eta_minutes
                    )
                )

            # Calculate total ride time (pickup + dropoff) and schedule completion
            drive_time = (ride_request.dropoff_location.calculate_distance_in_kilometer(ride_request.pickup_location) / 30) * 60
            completion_time = ride_request.timestamp + (pickup_eta_minutes * 60) + (drive_time * 60)
            best_driver.assign_ride(ride_request.id, completion_time)
            self._events_manager.add_event(RideCompletionEvent(completion_time, ride_request.id, best_driver))
            
        else:
            self.simulation_result.add_unassigned_ride(ride_request.id)
            
            
    def _process_ride_completion_event(self, ride_completion_event: RideCompletionEvent):
        """
        Process a ride completion event by freeing up the driver.
        
        Args:
            ride_completion_event (RideCompletionEvent): The ride completion event to process
        """
        ride_completion_event.driver.complete_ride()
        
    def run(self):
        """
        Execute the complete ride-sharing simulation.
        
        Processes all events in chronological order using the event manager.
        Each event is dispatched to its appropriate handler method based on
        the event type. The simulation continues until all events have been
        processed.
        """
        for event in self._events_manager.get_next_event_generator():
            try:
                event_type = event.__class__
                self._EVENT_TYPE_TO_HANDLER[event_type](event)
            except KeyError:
                print(f"No handler found for event: {event.__class__}")