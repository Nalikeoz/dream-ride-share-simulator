"""
Strategies package for driver selection algorithms.

This package contains different strategies for selecting the best driver
for a given ride request in the ride-sharing simulation.
"""

from .strategy_interface import StrategyInterface
from .straight_line_strategy import StraightLineStrategy
from .weighted_rating_strategy import WeightedRatingStrategy

__all__ = [
    "StrategyInterface",
    "StraightLineStrategy", 
    "WeightedRatingStrategy",
]
