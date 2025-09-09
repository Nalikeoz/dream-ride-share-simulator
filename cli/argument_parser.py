"""
Command-line argument parser for the ride-sharing simulator.
"""

import argparse
from typing import Any
from consts import StrategyType


class ArgumentParser:
    """
    Handles command-line argument parsing for the ride-sharing simulator.
    """
    
    @staticmethod
    def create_parser() -> argparse.ArgumentParser:
        """
        Create and configure the argument parser.
        
        Returns:
            argparse.ArgumentParser: Configured argument parser
        """
        parser = argparse.ArgumentParser(
            description="Ride-Sharing Simulation System",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Run with default straight-line strategy
  python3 main.py data.json -o results.json

  # Run with weighted rating strategy (default weights)
  python3 main.py data.json --strategy weighted -o results.json

  # Run with custom weights for weighted strategy
  python3 main.py data.json --strategy weighted --distance-weight 0.3 --rating-weight 0.7 -o results.json

  # Run with detailed output
  python3 main.py data.json --strategy weighted -o results.json --verbose
            """
        )
        
        # Required arguments
        parser.add_argument(
            'data_file',
            help='Path to the JSON data file containing drivers and ride requests'
        )
        
        # Strategy selection
        parser.add_argument(
            '--strategy', '-s',
            choices=[StrategyType.STRAIGHT, StrategyType.WEIGHTED],
            default=StrategyType.STRAIGHT,
            help='Driver selection strategy (default: straight)'
        )
        
        # Weighted strategy parameters
        parser.add_argument(
            '--distance-weight', '-d',
            type=float,
            default=0.6,
            help='Weight for distance component in weighted strategy (default: 0.6)'
        )
        
        parser.add_argument(
            '--rating-weight', '-r',
            type=float,
            default=0.4,
            help='Weight for rating component in weighted strategy (default: 0.4)'
        )
        
        # Output options
        parser.add_argument(
            '--output', '-o',
            help='Save JSON report to file (default: print to console)'
        )
        
        return parser
    
    @staticmethod
    def parse_arguments() -> argparse.Namespace:
        """
        Parse command line arguments.
        
        Returns:
            argparse.Namespace: Parsed command line arguments
        """
        parser = ArgumentParser.create_parser()
        return parser.parse_args()
