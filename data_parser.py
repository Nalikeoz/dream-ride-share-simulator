import json
from models.driver import Driver
from models.location import Location
from models.ride_request import RideRequest


class RideSimulationDataParser:
    """    
    This class handles loading and parsing of driver and ride request data
    from JSON files. It provides methods to extract drivers and ride requests
    from a structured JSON file format.
    
    Attributes:
        data_file_path (str): Path to the JSON data file containing the simulation data
    """
    
    def __init__(self, data_file_path: str):
        """        
        Args:
            data_file_path (str): Path to the JSON data file containing drivers and ride requests
        """
        self.data_file_path = data_file_path

    def get_drivers(self):
        """
        Load and parse drivers from the JSON data file.
        
        Opens the data file and extracts all driver records, converting them
        from JSON format to Driver objects. The method expects the JSON file
        to have a 'drivers' key containing a list of driver objects.
        
        Returns:
            list[Driver]: List of Driver objects parsed from the JSON data
        """
        with open(self.data_file_path, 'r') as f:
            data = json.load(f)
            return [
                self.driver_json_to_object(driver_json)
                for driver_json in data['drivers']
            ]
            
    def get_ride_requests(self):
        """
        Load and parse ride requests from the JSON data file.
        
        Opens the data file and extracts all ride request records, converting them
        from JSON format to RideRequest objects. The method expects the JSON file
        to have a 'ride_requests' key containing a list of ride request objects.
        
        Returns:
            list[RideRequest]: List of RideRequest objects parsed from the JSON data
        """
        with open(self.data_file_path, 'r') as f:
            data = json.load(f)
            return [
                self.ride_request_json_to_object(ride_request_json)
                for ride_request_json in data['ride_requests']
            ]
            
    def driver_json_to_object(self, driver_json: dict) -> Driver:
        """
        Convert driver JSON data to a Driver object.
        
        Takes a dictionary containing driver information and creates a Driver
        object with the appropriate attributes. The method expects the JSON
        to contain fields for id, name, vehicle_type, location, and rating.
        
        Args:
            driver_json (dict): Dictionary containing driver data from JSON
            
        Returns:
            Driver: Driver object with parsed attributes
            
        Expected JSON structure:
            {
                "id": "string",
                "name": "string", 
                "vehicle_type": "string",
                "location": {
                    "latitude": float,
                    "longitude": float
                },
                "rating": float
            }
        """
        return Driver(
            id=driver_json['id'],
            name=driver_json['name'],
            vehicle_type=driver_json['vehicle_type'],
            location=Location(
                latitude=driver_json['location']['latitude'],
                longitude=driver_json['location']['longitude']
            ),
            rating=driver_json['rating'])
        
    def ride_request_json_to_object(self, ride_request_json: dict) -> RideRequest:
        """
        Convert ride request JSON data to a RideRequest object.
        
        Takes a dictionary containing ride request information and creates a
        RideRequest object with the appropriate attributes. The method expects
        the JSON to contain fields for id, pickup location, dropoff location,
        requested vehicle type, timestamp, and user rating.
        
        Args:
            ride_request_json (dict): Dictionary containing ride request data from JSON
            
        Returns:
            RideRequest: RideRequest object with parsed attributes
            
        Expected JSON structure:
            {
                "id": "string",
                "pickup": {
                    "latitude": float,
                    "longitude": float
                },
                "dropoff": {
                    "latitude": float,
                    "longitude": float
                },
                "requested_vehicle_type": "string",
                "timestamp": float,
                "user_rating": float
            }
        """
        return RideRequest(
            id=ride_request_json['id'],
            pickup_location=Location(latitude=ride_request_json['pickup']['latitude'], longitude=ride_request_json['pickup']['longitude']),
            dropoff_location=Location(latitude=ride_request_json['dropoff']['latitude'], longitude=ride_request_json['dropoff']['longitude']),
            requested_vehicle_type=ride_request_json['requested_vehicle_type'],
            timestamp=ride_request_json['timestamp'],
            user_rating=ride_request_json['user_rating'])
