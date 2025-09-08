"""
Strategy Factory for creating driver selection strategies.

This module provides a centralized way to create strategy objects
with proper validation and configuration.
"""

from typing import Dict, Any, Type
from .strategy_interface import StrategyInterface
from .straight_line_strategy import StraightLineStrategy
from .weighted_rating_strategy import WeightedRatingStrategy


class StrategyFactory:
    """
    Factory class for creating driver selection strategies.
    
    This factory provides a centralized way to create strategy objects
    with proper validation and configuration management.
    """
    
    # Registry of available strategies with their parameter requirements
    _STRATEGY_REGISTRY: Dict[str, Dict[str, Any]] = {
        'straight': {
            'class': StraightLineStrategy,
            'required_params': [],
            'default_params': {}
        },
        'weighted': {
            'class': WeightedRatingStrategy,
            'required_params': ['distance_weight', 'rating_weight'],
            'default_params': {'distance_weight': 0.6, 'rating_weight': 0.4}
        }
    }
    
    @classmethod
    def create_strategy(cls, strategy_type: str, **kwargs) -> StrategyInterface:
        """
        Create a strategy instance based on the strategy type and parameters.
        
        Args:
            strategy_type (str): Type of strategy to create
            **kwargs: Additional parameters for strategy initialization
            
        Returns:
            StrategyInterface: Configured strategy instance
            
        Raises:
            ValueError: If strategy type is unknown or parameters are invalid
        """
        if strategy_type not in cls._STRATEGY_REGISTRY:
            available = ', '.join(cls._STRATEGY_REGISTRY.keys())
            raise ValueError(f"Unknown strategy type: '{strategy_type}'. Available: {available}")
        
        strategy_config = cls._STRATEGY_REGISTRY[strategy_type]
        strategy_class = strategy_config['class']
        
        # Validate parameters
        cls._validate_parameters(strategy_type, kwargs)
        
        # Build parameters: defaults + user provided
        final_params = {**strategy_config['default_params'], **kwargs}
        
        # Create and return strategy instance
        if final_params:
            return strategy_class(**final_params)
        else:
            return strategy_class()
    
    @classmethod
    def _validate_parameters(cls, strategy_type: str, params: Dict[str, Any]) -> None:
        """
        Validate parameters for the specified strategy type.
        
        Args:
            strategy_type (str): Type of strategy
            params (Dict[str, Any]): Parameters to validate
            
        Raises:
            ValueError: If parameters are invalid
        """
        strategy_config = cls._STRATEGY_REGISTRY[strategy_type]
        
        # Get final parameters (defaults + user provided)
        final_params = {**strategy_config['default_params'], **params}
        
        # Validate based on strategy type
        if strategy_type == 'weighted':
            distance_weight = final_params.get('distance_weight', 0.6)
            rating_weight = final_params.get('rating_weight', 0.4)
            
            if not (0.0 <= distance_weight <= 1.0):
                raise ValueError(f"Distance weight must be between 0.0 and 1.0, got {distance_weight}")
            
            if not (0.0 <= rating_weight <= 1.0):
                raise ValueError(f"Rating weight must be between 0.0 and 1.0, got {rating_weight}")
            
            # Check if weights sum to 1.0
            weight_sum = distance_weight + rating_weight
            if abs(weight_sum - 1.0) > 0.001:
                raise ValueError(f"Weights must sum to 1.0, got {weight_sum}")
    
    @classmethod
    def get_strategy_parameters(cls, strategy_type: str) -> Dict[str, Any]:
        """
        Get the required parameters for a strategy type.
        
        Args:
            strategy_type (str): Type of strategy
            
        Returns:
            Dict[str, Any]: Parameter information
        """
        if strategy_type == 'straight':
            return {
                'description': 'No parameters required',
                'parameters': {}
            }
        elif strategy_type == 'weighted':
            return {
                'description': 'Requires distance and rating weights',
                'parameters': {
                    'distance_weight': {
                        'type': 'float',
                        'range': [0.0, 1.0],
                        'default': 0.6,
                        'description': 'Weight for distance component'
                    },
                    'rating_weight': {
                        'type': 'float',
                        'range': [0.0, 1.0],
                        'default': 0.4,
                        'description': 'Weight for rating component'
                    }
                }
            }
        else:
            return {'description': 'Unknown strategy', 'parameters': {}}
