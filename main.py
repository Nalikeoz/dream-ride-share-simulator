from ride_share_simulator import RideShareSimulator
from pprint import pprint


if __name__ == "__main__":
    simulator = RideShareSimulator('datasets/sample_data.json')
    simulator.run()
    
    # Display the simulation results
    print("Simulation Results:")
    pprint(simulator.simulation_result.to_dict())