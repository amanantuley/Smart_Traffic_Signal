import time
import random
import csv
import os

# Function to simulate the number of vehicles at each road
def get_traffic_data():
    # Define mean and standard deviation for each road
    traffic_params = {
        'north': (25, 10),  # Mean 25, StdDev 10
        'south': (30, 15),  # Mean 30, StdDev 15
        'east': (20, 12),   # Mean 20, StdDev 12
        'west': (35, 8)     # Mean 35, StdDev 8
    }

    traffic_data = {}
    for road, (mean, std_dev) in traffic_params.items():
        # Generate vehicle count using a Gaussian distribution
        vehicles = int(random.gauss(mean, std_dev))

        # Ensure the count is within reasonable bounds (0 to 50)
        vehicles = max(0, min(vehicles, 50))
        traffic_data[road] = vehicles

    return traffic_data


# Function to calculate green light durations based on vehicle counts
def calculate_durations(traffic_data):
    base_duration = 10  # Base green signal duration in seconds
    max_duration = 40   # Maximum green signal duration in seconds
    min_duration = 5    # Minimum green signal duration in seconds

    # Get the maximum number of vehicles among all roads to scale the durations
    max_vehicles = max(traffic_data.values())

    durations = {}
    for road, vehicles in traffic_data.items():
        # Scale the duration proportionally to the number of vehicles
        duration = base_duration + (vehicles / max_vehicles) * (max_duration - base_duration)
        duration = max(min_duration, min(duration, max_duration))  # Ensure duration is within bounds
        durations[road] = int(duration)

    return durations


# Function to control the traffic signals
def control_traffic_signals(durations):
    for road, duration in durations.items():
        print(f"Green signal for {road} road for {duration} seconds.")
        # time.sleep(duration)
        print(f"Yellow signal for {road} road.")
        # time.sleep(5)  # Yellow signal duration for all roads
        print(f"Red signal for {road} road.")


# Function to save only green light durations to a CSV file
def save_durations_to_csv(durations, filename='traffic_data.csv'):
    # Ensure the static folder exists
    os.makedirs('static', exist_ok=True)
    file_path = os.path.join('static', filename)

    # Prepare the data to be written: durations only
    row_data = list(durations.values())
    
    # Write data to CSV file
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row_data)
        print(f"Green light durations saved to {file_path}: {row_data}")


# Main function to run the traffic signal control
def main():
    while True:
        traffic_data = get_traffic_data()  # Generate simulated traffic data
        print(f"Generated traffic data: {traffic_data}")

        durations = calculate_durations(traffic_data)  # Calculate durations for traffic signals
        control_traffic_signals(durations)  # Control the traffic signals

        # Save the green light durations to a CSV file
        save_durations_to_csv(durations)

        time.sleep(5)  # Wait before the next cycle

if __name__ == "__main__":
    main()
