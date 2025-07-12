# Run this on your computer
import serial
import csv
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# ---- CONFIGURATION ----
SERIAL_PORT = 'COM3'        # Replace with your port (Check on your Arduino IDE)
BAUD_RATE = 115200          # Arduino baudrate  (Check on your Arduino IDE)
CSV_FILENAME = '100768'     # change your filename here
max_len = 200               # x-axis lengh
TIMEOUT = 10800             # In seconds, how long to keep collecting data

# === SETUP ===
data = deque([0]*max_len, maxlen=max_len)
timestamps = deque([0]*max_len, maxlen=max_len)

# ---- OPEN SERIAL ----
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
    time.sleep(2)  # Wait for Arduino to reset
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# === SETUP CSV ===
csv_file = open(CSV_FILENAME, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Timestamp', 'Value'])  # Header

start_time = time.time()

# === PLOT SETUP ===
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(0, 32767) #min-max values y-axis
ax.set_xlim(0, max_len)
ax.set_title("Satellite finder voltage")
ax.set_xlabel("Samples")
ax.set_ylabel("Digital values")

def update(frame):
    current_time = time.time()
    if current_time - start_time > TIMEOUT:
        print(f"Finished after {TIMEOUT} seconds.")
        ani.event_source.stop()
        ser.close()
        csv_file.close()
        return line,

    try:
        raw = ser.readline().decode('utf-8').strip()
        if raw.isdigit():
            value = int(raw)
            timestamp = current_time - start_time
            data.append(value)
            timestamps.append(timestamp)
            csv_writer.writerow([round(timestamp, 2), value])
            line.set_ydata(data)
            line.set_xdata(range(len(data)))
    except UnicodeDecodeError:
        print("Decode error")
    except Exception as e:
        print(f"Error: {e}")

    return line,

ani = animation.FuncAnimation(fig, update, interval=100)
plt.tight_layout()
plt.show()