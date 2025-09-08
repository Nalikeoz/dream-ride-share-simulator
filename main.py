import argparse
import sys
import os
from ride_share_simulator import RideShareSimulator
from pprint import pprint


def parse_arguments():
    """
    Parse command line arguments for the ride-sharing simulator.
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Ride-Sharing Simulation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default straight-line strategy
  python main.py data.json

  # Run with weighted rating strategy (default weights)
  python main.py data.json --strategy weighted

  # Run with custom weights for weighted strategy
  python main.py data.json --strategy weighted --distance-weight 0.3 --rating-weight 0.7

  # Run with detailed output
  python main.py data.json --strategy weighted --verbose
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
        choices=['straight', 'weighted'],
        default='straight',
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
    
    # parser.add_argument(
    #     '--output', '-o',
    #     help='Save results to JSON file'
    # )
    
    return parser.parse_args()


def validate_arguments(args):
    """
    Validate the parsed arguments.
    
    Args:
        args (argparse.Namespace): Parsed arguments
        
    Raises:
        SystemExit: If validation fails
    """
    # Check if data file exists
    if not os.path.exists(args.data_file):
        print(f"Error: Data file '{args.data_file}' not found.")
        sys.exit(1)
    
    # Check if data file is JSON
    if not args.data_file.lower().endswith('.json'):
        print(f"Error: Data file must be a JSON file (.json extension).")
        sys.exit(1)
    
    # Validate weighted strategy weights
    if args.strategy == 'weighted':
        if not (0.0 <= args.distance_weight <= 1.0):
            print(f"Error: Distance weight must be between 0.0 and 1.0, got {args.distance_weight}")
            sys.exit(1)
        
        if not (0.0 <= args.rating_weight <= 1.0):
            print(f"Error: Rating weight must be between 0.0 and 1.0, got {args.rating_weight}")
            sys.exit(1)
        
        # Check if weights sum to 1.0
        weight_sum = args.distance_weight + args.rating_weight
        if abs(weight_sum - 1.0) > 0.001:
            print(f"Warning: Distance and rating weights sum to {weight_sum:.3f}, not 1.0")
            print("This may produce unexpected results.")




def print_simulation_info(args):
    """
    Print simulation configuration information.
    
    Args:
        args (argparse.Namespace): Parsed arguments
    """
    print("=" * 80)
    print("RIDE-SHARING SIMULATION")
    print("=" * 80)
    print(f"Data File: {args.data_file}")
    print(f"Strategy: {args.strategy.title()}")
    
    if args.strategy == 'weighted':
        print(f"Distance Weight: {args.distance_weight}")
        print(f"Rating Weight: {args.rating_weight}")
    
    print("-" * 80)


def run_simulation(args):
    """
    Run the simulation with the specified configuration.
    
    Args:
        args (argparse.Namespace): Parsed arguments
        
    Returns:
        RideShareSimulator: The completed simulation
    """
    # Create simulator with strategy parameters
    simulator = RideShareSimulator(
        data_file_path=args.data_file,
        strategy_type=args.strategy,
        distance_weight=args.distance_weight,
        rating_weight=args.rating_weight
    )
    
    # Run simulation
    simulator.run()
    
    return simulator


def print_results(simulator, args):
    """
    Print simulation results.
    
    Args:
        simulator (RideShareSimulator): The completed simulation
        args (argparse.Namespace): Parsed arguments
    """
    results = simulator.simulation_result.to_dict()
    
    print("\n" + "=" * 80)
    print("SIMULATION RESULTS")
    print("=" * 80)
    
    # Summary metrics
    print(f"Total Rides: {results['metrics']['total_rides']}")
    print(f"Successful Assignments: {results['metrics']['assigned_rides']}")
    print(f"Unassigned Rides: {results['metrics']['unassigned_rides']}")
    print(f"Assignment Rate: {results['metrics']['assignment_rate_percent']:.1f}%")
    print(f"Average Pickup ETA: {results['metrics']['average_pickup_eta_minutes']:.2f} minutes")


def main():
    """
    Main entry point for the ride-sharing simulator.
    """
    try:
        # Parse and validate arguments
        args = parse_arguments()
        validate_arguments(args)
        
        # Print simulation info
        print_simulation_info(args)
        
        # Run simulation
        simulator = run_simulation(args)
        
        # Print results
        print_results(simulator, args)
        
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()