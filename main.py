"""
Main entry point for the ride-sharing simulator.

This module provides the main entry point and orchestrates the simulation
process using the CLI modules for argument parsing, validation, and output
formatting.
"""

import sys
from cli import ArgumentParser, ArgumentValidator, OutputFormatter
from ride_share_simulator import RideShareSimulator


def main():
    """
    Main entry point for the ride-sharing simulator.
    
    Orchestrates the complete simulation process:
    1. Parse command-line arguments
    2. Validate arguments
    3. Run simulation
    4. Output JSON report
    """
    # Parse and validate arguments
    args = ArgumentParser.parse_arguments()
    ArgumentValidator.validate_arguments(args)
    
    # Run simulation
    # Create simulator with strategy parameters
    simulator = RideShareSimulator(
        data_file_path=args.data_file,
        strategy_type=args.strategy,
        distance_weight=args.distance_weight,
        rating_weight=args.rating_weight
    )
    
    # Run simulation
    simulator.run()
    
    # Output JSON report
    if args.output:
        OutputFormatter.save_json_report(simulator, args.output)
    else:
        OutputFormatter.print_json_report(simulator)

if __name__ == "__main__":
    main()