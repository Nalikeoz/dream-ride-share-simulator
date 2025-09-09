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
python3 main.py datasets/sample_data.json

# Run with weighted rating strategy (default weights: 60% distance, 40% rating)
python3 main.py datasets/sample_data.json --strategy weighted
```

### Advanced Usage

```bash
# Custom weights for weighted strategy (30% distance, 70% rating)
python3 main.py datasets/sample_data.json --strategy weighted --distance-weight 0.3 --rating-weight 0.7

# Save results to file
python3 main.py datasets/sample_data.json --strategy weighted --output results.json
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--strategy` | `-s` | Driver selection strategy (`straight` or `weighted`) | `straight` |
| `--distance-weight` | `-d` | Weight for distance component (0.0-1.0) | `0.6` |
| `--rating-weight` | `-r` | Weight for rating component (0.0-1.0) | `0.4` |
| `--output` | `-o` | Save results to JSON file | None |

### Help

```bash
python3 main.py --help
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
      "location": {"latitude": 32.0853, "longitude": 34.7818},
      "rating": 4.8
    }
  ],
  "ride_requests": [
    {
      "id": "ride_001",
      "pickup": {"latitude": 32.0943, "longitude": 34.7818},
      "dropoff": {"latitude": 40.7000, "longitude": -100.0000},
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

The simulation outputs a JSON report containing:

- **Assignments**: Array of successful ride assignments with timestamp, ride_id, and driver_id
- **Unassigned Rides**: Array of ride IDs that could not be assigned to drivers
- **Metrics**: Average pickup ETA in minutes

Example output:
```json
{
  "assignments": [
    {
      "timestamp": 1640995200.0,
      "ride_id": "ride_001",
      "driver_id": "driver_001"
    }
  ],
  "unassigned_rides": [
    "ride_005",
    "ride_006"
  ],
  "metrics": {
    "average_pickup_eta_minutes": 143.09
  }
}
```

## Examples

### Compare Strategies

```bash
# Run with straight-line strategy
python3 main.py datasets/sample_data.json --strategy straight --output straight_results.json

# Run with weighted strategy
python3 main.py datasets/sample_data.json --strategy weighted --output weighted_results.json

# Compare the results
```

### Test Different Weight Configurations

```bash
# Distance-focused (80% distance, 20% rating)
python3 main.py datasets/sample_data.json --strategy weighted --distance-weight 0.8 --rating-weight 0.2

# Rating-focused (20% distance, 80% rating)
python3 main.py datasets/sample_data.json --strategy weighted --distance-weight 0.2 --rating-weight 0.8

# Balanced (50% distance, 50% rating)
python3 main.py datasets/sample_data.json --strategy weighted --distance-weight 0.5 --rating-weight 0.5
```

## Error Handling

The system provides clear error messages for:

- Missing or invalid data files
- Invalid strategy parameters
- Malformed JSON data
- Invalid weight values (must be between 0.0 and 1.0)
- Weight sum validation (warns if weights don't sum to 1.0)

## Performance

- **Small datasets** (< 100 rides): Runs in milliseconds
- **Medium datasets** (100-1000 rides): Runs in seconds
- **Large datasets** (> 1000 rides): Performance depends on driver availability and strategy complexity

## Contributing

To add new strategies:

1. Create a new strategy class in `strategies/` directory
2. Implement the `StrategyInterface`
3. Add the strategy to the command-line options in `cli/argument_parser.py`
4. Update this README with usage examples
