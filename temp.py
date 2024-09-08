import tkinter as tk
import pandas as pd
import time
from threading import Thread

class TrafficLightApp:
    def __init__(self, master, green_durations):
        self.master = master
        self.green_durations = green_durations
        self.red_duration = sum(green_durations) + 20
        
        # Create labels for timers
        self.labels = []
        for i in range(4):
            label = tk.Label(master, font=("Helvetica", 48), width=10)
            label.grid(row=i, column=0)
            self.labels.append(label)

        self.start_timers()

    def start_timers(self):
        # Start threads for each road timer
        for i in range(4):
            Thread(target=self.run_timer, args=(i,)).start()

    def run_timer(self, road_index):
        green_duration = self.green_durations[road_index]

        # Green light for the current road
        for t in range(green_duration, 0, -1):
            self.labels[road_index].config(text=f'Road {road_index + 1}\nGreen\n{t}')
            for j in range(4):
                if j != road_index:
                    # Show red for the other roads
                    self.labels[j].config(text=f'Road {j + 1}\nRed\n{self.red_duration}')
            time.sleep(1)

        # Yellow light (fixed duration)
        for t in range(5, 0, -1):
            self.labels[road_index].config(text=f'Road {road_index + 1}\nYellow\n{t}')
            for j in range(4):
                if j != road_index:
                    # Show red for the other roads
                    self.labels[j].config(text=f'Road {j + 1}\nRed\n{self.red_duration}')
            time.sleep(1)

        # Red light for the current road
        for t in range(self.red_duration, 0, -1):
            for j in range(4):
                if j == road_index:
                    self.labels[j].config(text=f'Road {j + 1}\nRed\n{t}')
                else:
                    remaining_time = self.red_duration - (self.green_durations[j] + 5) + (self.red_duration - t)
                    self.labels[j].config(text=f'Road {j + 1}\nRed\n{remaining_time}')
            time.sleep(1)

def main():
    # Load green light durations from CSV
    df = pd.read_csv(r'C:\Users\MOIN\Desktop\MiniProject\static\traffic_data.csv', header=None)
    green_durations = df.iloc[0].tolist()  # Get the first row as a list

    # Initialize red duration for the other roads based on the green light durations
    global red_duration
    red_duration = sum(green_durations) + 20

    root = tk.Tk()
    root.title("Traffic Light Timers")
    app = TrafficLightApp(root, green_durations)
    root.mainloop()

if __name__ == "__main__":
    main()
