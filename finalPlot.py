import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Initialize the sensor value lists
pH1_values = []
pH2_values = []
CO2_values = []
TDS_values = []
water_temp_values = []
air_temp_values = []
humidity_values = []

# Set up the serial connection (make sure to adjust the port)
ser = serial.Serial('COM3', 9600, timeout=1)  # Replace 'COM3' with the correct port
time.sleep(2)  # Wait for the connection to initialize

(i, c) = (1, 1)

# Create a figure and axes for the 3x2 grid
fig, axs = plt.subplots(3, 2, figsize=(10, 8))

# Set the main title
fig.suptitle('Aquaponics', fontsize=16)

# Adjust the layout to add proper spacing between subplots
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.5, wspace=0.3)

# Function to update the plots dynamically
def update(frame):
    for ax in axs.flat:
        ax.clear()  # Clear previous frame

    # Plot each sensor's values, calculate the average, and display it with spacing
    if pH1_values:
        avg_pH1 = np.mean(pH1_values)
        axs[0, 0].plot(pH1_values,'r-', label="pH1", linewidth=2, marker='o', markersize=4)
        axs[0, 0].text(0.5, 1.05, f"Avg: {avg_pH1:.2f}", ha='center', va='center', transform=axs[0, 0].transAxes, fontsize=10)  # Add space above the title
        axs[0, 0].set_title("pH1 Sensor", pad=20)  # Add space below the avg value
        axs[0, 0].legend()
        axs[0, 0].grid(True)

    if pH2_values:
        avg_pH2 = np.mean(pH2_values)
        axs[0, 1].plot(pH2_values,'g-', label="pH2", linewidth=2, marker='o', markersize=4)
        axs[0, 1].text(0.5, 1.05, f"Avg: {avg_pH2:.2f}", ha='center', va='center', transform=axs[0, 1].transAxes, fontsize=10)
        axs[0, 1].set_title("pH2 Sensor", pad=20)
        axs[0, 1].legend()
        axs[0, 1].grid(True)

    if CO2_values:
        avg_CO2 = np.mean(CO2_values)
        axs[1, 0].plot(CO2_values,'o-', label="CO2", linewidth=2, marker='o', markersize=4)
        axs[1, 0].text(0.5, 1.05, f"Avg: {avg_CO2:.2f}", ha='center', va='center', transform=axs[1, 0].transAxes, fontsize=10)
        axs[1, 0].set_title("CO2 Sensor", pad=20)
        axs[1, 0].legend()
        axs[1, 0].grid(True)

    if TDS_values:
        avg_TDS = np.mean(TDS_values)
        axs[1, 1].plot(TDS_values, 'b-',label="TDS", linewidth=2, marker='o', markersize=4)
        axs[1, 1].text(0.5, 1.05, f"Avg: {avg_TDS:.2f}", ha='center', va='center', transform=axs[1, 1].transAxes, fontsize=10)
        axs[1, 1].set_title("TDS Sensor", pad=20)
        axs[1, 1].legend()
        axs[1, 1].grid(True)

    if water_temp_values and air_temp_values:
        avg_water_temp = np.mean(water_temp_values)
        avg_air_temp = np.mean(air_temp_values)
        axs[2, 0].plot(water_temp_values, 'c-', label="Water Temp", linewidth=2, marker='o', markersize=4)
        axs[2, 0].plot(air_temp_values,'m-', label="Air Temp", linewidth=2, marker='o', markersize=4)
        axs[2, 0].text(0.5, 1.05, f"Water Avg: {avg_water_temp:.2f}, Air Avg: {avg_air_temp:.2f}", 
                       ha='center', va='center', transform=axs[2, 0].transAxes, fontsize=10)
        axs[2, 0].set_title("Water Temp & Air Temp", pad=20)
        axs[2, 0].legend()
        axs[2, 0].grid(True)

    if humidity_values:
        avg_humidity = np.mean(humidity_values)
        axs[2, 1].plot(humidity_values, label="Humidity", linewidth=2, marker='o', markersize=4)
        axs[2, 1].text(0.5, 1.05, f"Avg: {avg_humidity:.2f}", ha='center', va='center', transform=axs[2, 1].transAxes, fontsize=10)
        axs[2, 1].set_title("Humidity", pad=20)
        axs[2, 1].legend()
        axs[2, 1].grid(True)

# Function to read and process serial data
def read_serial():
    global c, i
    try:
        data = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
        
        if data and i != 1:
            print(data)
            # Split and process data, with error handling for missing data
            if c % 6 == 1:
                pH1 = float(data.split(': ')[1].strip())
                pH1_values.append(pH1)
            elif c % 6 == 2:
                pH2 = float(data.split(': ')[1].strip())
                pH2_values.append(pH2)
            elif c % 6 == 3:
                co2 = float(data.split(': ')[1].strip())
                CO2_values.append(co2)
            elif c % 6 == 4:
                tds = float(data.split(': ')[1].strip())
                TDS_values.append(tds)
            elif c % 6 == 5:
                Wtemp = float(data.split(': ')[1].strip()[:-2])
                water_temp_values.append(Wtemp)
            elif c % 6 == 0:
                line = data.split("\t\t")
                Atemp = float(line[0].split(': ')[1].strip()[:-2])
                Humid = float(line[1].split(': ')[1].strip()[:-2])
                air_temp_values.append(Atemp)
                humidity_values.append(Humid)

            # Keep list sizes under control (max 10 data points)
            if len(pH1_values) >= 15:
                pH1_values.pop(0)
            if len(pH2_values) >= 15:
                pH2_values.pop(0)
            if len(CO2_values) >= 15:
                CO2_values.pop(0)
            if len(TDS_values) >= 15:
                TDS_values.pop(0)
            if len(water_temp_values) >= 15:
                water_temp_values.pop(0)
            if len(air_temp_values) >= 15:
                air_temp_values.pop(0)
            if len(humidity_values) >= 15:
                humidity_values.pop(0)

            c += 1
        i += 1
    except KeyboardInterrupt:
        print("Exiting...")
        ser.close()

# Set up the animation, with cache disabled to avoid the warning
ani = animation.FuncAnimation(fig, update, interval=1000, cache_frame_data=False)

# Read data continuously and update the plot
try:
    while True:
        read_serial()  # Read data from the serial port
        plt.pause(0.001)  # Brief pause to allow the plot to update
except KeyboardInterrupt:
    print("Exiting...")
    ser.close()

plt.tight_layout()
plt.grid(True)
plt.show()
