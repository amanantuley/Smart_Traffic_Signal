import csv
from collections import deque
import time

csv_file = r'C:\Users\MOIN\Desktop\MiniProject\static\traffic_data.csv'

# Load the entire CSV into memory
with open(csv_file, newline='') as file:
    reader = csv.reader(file)
    data = [list(map(int, row)) for row in reader]  # Convert to a list of lists of integers

# Create a deque with a flexible size to hold the sliding window
sliding_window = deque(maxlen=12)  # Keep the last 12 elements in the sliding window

# Initialize a list to hold the countdown durations for 4 r values
countdown_durations = [0] * 4  # Four countdown values initialized to 0
countdown_started = False  # Flag to check if countdown has started
countdown_index = 0  # Index to track which countdown is currently active

# Loop through the entire data continuously
while True:
    for row in data:
        for value in row:
            sliding_window.append(value)

            # Ensure the sliding window has enough terms to calculate the r values
            if len(sliding_window) >= 12 and not countdown_started:
                # Calculate r values for the first four overlapping sets of four elements
                for i in range(0, 4):  # Only calculate the first four sets
                    if i + 4 <= len(sliding_window):  # Ensure there are enough elements to slice
                        g1_1, g1_2, g1_3, g1_4 = list(sliding_window)[i:i + 4]
                        r = sum(list(sliding_window)[i:i + 4]) + 15 - g1_1

                        # Assign the calculated r to the corresponding countdown duration
                        countdown_durations[i] = r

                # Start the countdowns
                countdown_started = True
                print("Initial countdowns:", countdown_durations)

            # Print the current countdown durations for the four r values
            if countdown_started:
                print(f'Countdowns: {countdown_durations[0]} seconds, {countdown_durations[1]} seconds, '
                      f'{countdown_durations[2]} seconds, {countdown_durations[3]} seconds')

                # Check if the active countdown reaches zero
                if countdown_durations[countdown_index] > 0:
                    countdown_durations[countdown_index] -= 1  # Decrement the countdown value

                # Check if the current countdown has finished
                if countdown_durations[countdown_index] <= 0:
                    print(f"Countdown {countdown_index + 1} finished!")
                    countdown_index += 1  # Move to the next countdown

                    # Check if there are more countdowns to calculate
                    if countdown_index < 4:
                        # Calculate the next r value for the next countdown
                        next_r_index = countdown_index + 4  # Next overlapping set index
                        if next_r_index + 4 <= len(sliding_window):
                            g1_1, g1_2, g1_3, g1_4 = list(sliding_window)[next_r_index:next_r_index + 4]
                            r = sum(list(sliding_window)[next_r_index:next_r_index + 4]) + 15 - g1_1
                            countdown_durations[countdown_index] = r
                            print(f"Next countdown set to: {countdown_durations[countdown_index]} seconds")

                print()  # Print a newline for better readability

                time.sleep(1)  # Add a delay to simulate continuous reading

            # Break if all countdowns have finished
            if countdown_index >= 4:
                break

        if countdown_index >= 4:
            break

    if countdown_index >= 4:
        break  # Exit the outer loop if all countdowns have finished
