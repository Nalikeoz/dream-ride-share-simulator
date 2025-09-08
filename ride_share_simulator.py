from strategies.straight_line_strategy import StraightLineStrategy
from models.simulation_result import SimulationResult
from events_manager import EventsManager
from events.ride_request_event import RideRequestEvent
from events.ride_completion_event import RideCompletionEvent
from data_parser import RideSimulationDataParser
from models.assignment import Assignment
from pprint import pprint


class RideShareSimulator:
    """
    Main simulation engine for the ride-sharing system.
    
    The RideShareSimulator orchestrates the entire simulation process by managing
    events, drivers, and ride requests. It uses a discrete event simulation approach
    where events are processed in chronological order to simulate the real-time
    operation of a ride-sharing platform.
    
    """
    def __init__(self, data_file_path: str):
        """
        Initialize the RideShareSimulator with data from the specified file.
        
        Args:
            data_file_path (str): Path to the JSON file containing drivers and ride requests
        """
        self.strategy = StraightLineStrategy()
        self.simulation_result = SimulationResult()

        self.data_parser = RideSimulationDataParser(data_file_path)
        self._events_manager = EventsManager()
        self.drivers = self.data_parser.get_drivers()
        
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
        print(f"Processing ride request event: {ride_request_event.ride_request.id}")
        ride_request = ride_request_event.ride_request
        best_driver = self.strategy.get_best_driver(ride_request, self.drivers)
        
        if best_driver:
            # Calculate pickup ETA assuming average speed of 30 km/h
            pickup_eta_minutes = best_driver.location.calculate_distance_in_kilometer(ride_request.pickup_location) / 30
            self.simulation_result.add_assignment(
                Assignment(
                    timestamp=ride_request.timestamp,
                    ride_id=ride_request.id,
                    driver_id=best_driver.id,
                    pickup_eta_minutes=pickup_eta_minutes
                    )
                )

            # Calculate total ride time (pickup + dropoff) and schedule completion
            drive_time = ride_request.dropoff_location.calculate_distance_in_kilometer(ride_request.pickup_location) / 30
            completion_time = ride_request.timestamp + pickup_eta_minutes + drive_time
            best_driver.assign_ride(ride_request.id, completion_time)
            self._events_manager.add_event(RideCompletionEvent(completion_time, ride_request.id, best_driver))
            
        else:
            print(f"No driver found for ride request: {ride_request.id}")
            self.simulation_result.add_unassigned_ride(ride_request.id)
            
            
    def _process_ride_completion_event(self, ride_completion_event: RideCompletionEvent):
        """
        Process a ride completion event by freeing up the driver.
        
        Args:
            ride_completion_event (RideCompletionEvent): The ride completion event to process
        """
        print(f"Processing ride completion event: {ride_completion_event.driver.id}")
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
                
