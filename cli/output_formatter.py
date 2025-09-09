"""
Output formatting for the ride-sharing simulator.
"""

import json
from typing import Any, Dict, List
from argparse import Namespace
from ride_share_simulator import RideShareSimulator


class OutputFormatter:
    """
    Handles formatting and display of simulation information and results.
    """
    
    @staticmethod
    def generate_json_report(simulator: RideShareSimulator) -> Dict[str, Any]:
        """
        Generate a JSON report with assignments, unassigned rides, and metrics.
        
        Args:
            simulator (RideShareSimulator): The completed simulation
            
        Returns:
            Dict[str, Any]: JSON report structure
        """
        results = simulator.simulation_result.to_dict()
        
        # Extract assignments with required fields
        assignments = []
        for assignment in results.get('assignments', []):
            assignments.append({
                'timestamp': assignment['timestamp'],
                'ride_id': assignment['ride_id'],
                'driver_id': assignment['driver_id']
            })
        
        # Extract unassigned ride IDs
        unassigned_rides = results.get('unassigned_ride_ids', [])
        
        # Extract metrics
        metrics = results.get('metrics', {})
        average_pickup_eta = metrics.get('average_pickup_eta_minutes', 0.0)
        
        # Build JSON report
        report = {
            'assignments': assignments,
            'unassigned_rides': unassigned_rides,
            'metrics': {
                'average_pickup_eta_minutes': round(average_pickup_eta, 2)
            }
        }
        
        return report
    
    @staticmethod
    def print_json_report(simulator: RideShareSimulator) -> None:
        """
        Print simulation results as JSON.
        
        Args:
            simulator (RideShareSimulator): The completed simulation
        """
        report = OutputFormatter.generate_json_report(simulator)
        print(json.dumps(report, indent=2))
    
    @staticmethod
    def save_json_report(simulator: RideShareSimulator, filename: str) -> None:
        """
        Save simulation results as JSON to a file.
        
        Args:
            simulator (RideShareSimulator): The completed simulation
            filename (str): Output filename
        """
        report = OutputFormatter.generate_json_report(simulator)
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
    