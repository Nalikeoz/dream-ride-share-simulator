from dataclasses import dataclass, field
from typing import List, Dict, Any
from .assignment import Assignment


@dataclass
class SimulationResult:
    assignments: List[Assignment] = field(default_factory=list)
    unassigned_ride_ids: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    def add_assignment(self, assignment: Assignment) -> None:
        """
        Add a new assignment to the results.
        
        Args:
            assignment (Assignment): The assignment to add
        """
        self.assignments.append(assignment)
    
    def add_unassigned_ride(self, ride_id: str) -> None:
        """
        Add a ride ID to the unassigned rides list.
        
        Args:
            ride_id (str): ID of the unassigned ride
        """
        self.unassigned_ride_ids.append(ride_id)
    
    def set_metric(self, key: str, value: Any) -> None:
        """
        Set a metric value.
        
        Args:
            key (str): Metric name
            value (Any): Metric value
        """
        self.metrics[key] = value
    
    def get_metric(self, key: str, default: Any = None) -> Any:
        """
        Get a metric value.
        
        Args:
            key (str): Metric name
            default (Any): Default value if metric doesn't exist
            
        Returns:
            Any: Metric value or default
        """
        return self.metrics.get(key, default)
    
    def calculate_average_pickup_eta(self) -> float:
        """
        Calculate the average pickup ETA across all assignments.
        
        Returns:
            float: Average pickup ETA in minutes, or 0.0 if no assignments
        """
        if not self.assignments:
            return 0.0
        
        total_eta = sum(assignment.pickup_eta_minutes for assignment in self.assignments)
        return total_eta / len(self.assignments)
    
    def get_assignment_count(self) -> int:
        """
        Get the total number of successful assignments.
        
        Returns:
            int: Number of assignments
        """
        return len(self.assignments)
    
    def get_unassigned_count(self) -> int:
        """
        Get the total number of unassigned rides.
        
        Returns:
            int: Number of unassigned rides
        """
        return len(self.unassigned_ride_ids)
    
    def get_total_rides(self) -> int:
        """
        Get the total number of rides processed.
        
        Returns:
            int: Total number of rides
        """
        return self.get_assignment_count() + self.get_unassigned_count()
    
    def get_assignment_rate(self) -> float:
        """
        Get the percentage of rides that were successfully assigned.
        
        Returns:
            float: Assignment rate as a percentage (0.0 to 100.0)
        """
        total_rides = self.get_total_rides()
        if total_rides == 0:
            return 0.0
        
        return (self.get_assignment_count() / total_rides) * 100.0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the simulation result to a dictionary for JSON serialization.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the result
        """
        return {
            "assignments": [
                {
                    "timestamp": assignment.timestamp,
                    "ride_id": assignment.ride_id,
                    "driver_id": assignment.driver_id,
                    "pickup_eta_minutes": assignment.pickup_eta_minutes,
                }
                for assignment in self.assignments
            ],
            "unassigned_ride_ids": self.unassigned_ride_ids,
            "metrics": {
                **self.metrics,
                "total_rides": self.get_total_rides(),
                "assigned_rides": self.get_assignment_count(),
                "unassigned_rides": self.get_unassigned_count(),
                "assignment_rate_percent": self.get_assignment_rate(),
                "average_pickup_eta_minutes": self.calculate_average_pickup_eta()
            }
        }
