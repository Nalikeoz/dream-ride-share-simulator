# Ride-Sharing Simulation System

A discrete event simulation system for ride-sharing platforms that supports different driver selection strategies.

## Features

- **Multiple Strategies**: Straight-line distance and weighted rating-based matching
- **Configurable Parameters**: Customize strategy weights and parameters
- **Console Interface**: Easy-to-use command-line interface
- **Detailed Results**: Comprehensive simulation metrics and reporting
- **JSON Output**: Save results to files for further analysis

## Installation

1. Clone or download the project
2. Ensure you have Python 3.7+ installed
3. No additional dependencies required (uses only standard library)

## Usage

### Basic Usage

```bash
# Run simulation with default straight-line strategy
python main.py datasets/sample_data.json

# Run with weighted rating strategy (default weights: 60% distance, 40% rating)
python main.py datasets/sample_data.json --strategy weighted
```

### Advanced Usage

```bash
# Custom weights for weighted strategy (30% distance, 70% rating)
python main.py datasets/sample_data.json --strategy weighted --distance-weight 0.3 --rating-weight 0.7

# Save results to file
python main.py datasets/sample_data.json --strategy weighted --output results.json

# Verbose output with detailed information
python main.py datasets/sample_data.json --strategy weighted --verbose

# Quiet mode (suppress progress output)
python main.py datasets/sample_data.json --strategy weighted --quiet
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--strategy` | `-s` | Driver selection strategy (`straight` or `weighted`) | `straight` |
| `--distance-weight` | `-d` | Weight for distance component (0.0-1.0) | `0.6` |
| `--rating-weight` | `-r` | Weight for rating component (0.0-1.0) | `0.4` |
| `--verbose` | `-v` | Show detailed simulation output | `False` |
| `--quiet` | `-q` | Suppress simulation progress output | `False` |
| `--output` | `-o` | Save results to JSON file | None |

### Help

```bash
python main.py --help
```

## Data Format

The simulation expects a JSON file with the following structure:

```json
{
  "drivers": [
    {
      "id": "driver_001",
      "name": "Alice Johnson",
      "vehicle_type": "private",
      "location": {"latitude": 40.0, "longitude": -70.0},
      "rating": 4.8
    }
  ],
  "ride_requests": [
    {
      "id": "ride_001",
      "pickup": {"latitude": 40.7, "longitude": -74.0},
      "dropoff": {"latitude": 40.7, "longitude": -100.0},
      "requested_vehicle_type": "private",
      "timestamp": 1640995200.0,
      "user_rating": 4.7
    }
  ]
}
```

### Data Requirements

- **Drivers**: Must have `id`, `name`, `vehicle_type`, `location`, and `rating`
- **Ride Requests**: Must have `id`, `pickup`, `dropoff`, `requested_vehicle_type`, `timestamp`, and `user_rating`
- **Vehicle Types**: Must be `"private"` or `"suv"`
- **Ratings**: Must be between 0.0 and 5.0
- **Timestamps**: Unix timestamp (seconds since epoch)

## Strategies

### Straight Line Strategy
- **Description**: Selects the closest available driver
- **Use Case**: Minimizes pickup time
- **Parameters**: None

### Weighted Rating Strategy
- **Description**: Balances distance and rating compatibility
- **Use Case**: Matches higher-rated users with higher-rated drivers
- **Parameters**:
  - `distance_weight`: How much to prioritize distance (0.0-1.0)
  - `rating_weight`: How much to prioritize rating matching (0.0-1.0)
  - Weights should sum to 1.0 for best results

## Output

The simulation provides:

- **Assignment Rate**: Percentage of successful ride assignments
- **Average Pickup ETA**: Average time to pickup in minutes
- **Total Metrics**: Counts of rides, assignments, and unassigned rides
- **Detailed Results**: Complete assignment details (with `--verbose`)

### Example Output

```
================================================================================
RIDE-SHARING SIMULATION
================================================================================
Data File: datasets/sample_data.json
Strategy: Weighted
Distance Weight: 0.3
Rating Weight: 0.7
--------------------------------------------------------------------------------

================================================================================
SIMULATION RESULTS
================================================================================
Total Rides: 5
Successful Assignments: 5
Unassigned Rides: 0
Assignment Rate: 100.0%
Average Pickup ETA: 2.45 minutes
```

## Examples

### Compare Strategies

```bash
# Run with straight-line strategy
python main.py datasets/sample_data.json --strategy straight --output straight_results.json

# Run with weighted strategy
python main.py datasets/sample_data.json --strategy weighted --output weighted_results.json

# Compare the results
```

### Test Different Weight Configurations

```bash
# Distance-focused (80% distance, 20% rating)
python main.py datasets/sample_data.json --strategy weighted --distance-weight 0.8 --rating-weight 0.2

# Rating-focused (20% distance, 80% rating)
python main.py datasets/sample_data.json --strategy weighted --distance-weight 0.2 --rating-weight 0.8

# Balanced (50% distance, 50% rating)
python main.py datasets/sample_data.json --strategy weighted --distance-weight 0.5 --rating-weight 0.5
```

## Error Handling

The system provides clear error messages for:

- Missing or invalid data files
- Invalid strategy parameters
- Malformed JSON data
- Invalid weight values

## Performance

- **Small datasets** (< 100 rides): Runs in milliseconds
- **Medium datasets** (100-1000 rides): Runs in seconds
- **Large datasets** (> 1000 rides): Performance depends on driver availability and strategy complexity

## Contributing

To add new strategies:

1. Create a new strategy class in `strategies/` directory
2. Implement the `StrategyInterface`
3. Add the strategy to the command-line options in `main.py`
4. Update this README with usage examples
