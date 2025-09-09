"""
Argument validation for the ride-sharing simulator.
"""

import os
import sys
from typing import Any
from argparse import Namespace
from consts import StrategyType


class ArgumentValidator:
    """
    Handles validation of command-line arguments.
    """
    
    @staticmethod
    def validate_arguments(args: Namespace) -> None:
        """
        Validate the parsed arguments.
        
        Args:
            args (argparse.Namespace): Parsed arguments
            
        Raises:
            SystemExit: If validation fails
        """
        ArgumentValidator._validate_data_file(args.data_file)
        ArgumentValidator._validate_strategy_weights(args)
    
    @staticmethod
    def _validate_data_file(data_file: str) -> None:
        """
        Validate the data file argument.
        
        Args:
            data_file (str): Path to the data file
            
        Raises:
            SystemExit: If validation fails
        """
        # Check if data file exists
        if not os.path.exists(data_file):
            print(f"Error: Data file '{data_file}' not found.")
            sys.exit(1)
        
        # Check if data file is JSON
        if not data_file.lower().endswith('.json'):
            print(f"Error: Data file must be a JSON file (.json extension).")
            sys.exit(1)
    
    @staticmethod
    def _validate_strategy_weights(args: Namespace) -> None:
        """
        Validate strategy-specific weight parameters.
        
        Args:
            args (argparse.Namespace): Parsed arguments
            
        Raises:
            SystemExit: If validation fails
        """
        if args.strategy == StrategyType.WEIGHTED:
            ArgumentValidator._validate_weight_range(
                args.distance_weight, 'Distance weight'
            )
            ArgumentValidator._validate_weight_range(
                args.rating_weight, 'Rating weight'
            )
            ArgumentValidator._validate_weight_sum(
                args.distance_weight, args.rating_weight
            )
    
    @staticmethod
    def _validate_weight_range(weight: float, weight_name: str) -> None:
        """
        Validate that a weight is within the valid range [0.0, 1.0].
        
        Args:
            weight (float): Weight value to validate
            weight_name (str): Name of the weight for error messages
            
        Raises:
            SystemExit: If validation fails
        """
        if not (0.0 <= weight <= 1.0):
            print(f"Error: {weight_name} must be between 0.0 and 1.0, got {weight}")
            sys.exit(1)
    
    @staticmethod
    def _validate_weight_sum(distance_weight: float, rating_weight: float) -> None:
        """
        Validate that weights sum to approximately 1.0.
        
        Args:
            distance_weight (float): Distance weight
            rating_weight (float): Rating weight
            
        Raises:
            SystemExit: If validation fails
        """
        weight_sum = distance_weight + rating_weight
        if abs(weight_sum - 1.0) > 0.001:
            print(f"Warning: Distance and rating weights sum to {weight_sum:.3f}, not 1.0")
            print("This may produce unexpected results.")
    
