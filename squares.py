import sys
import threading
import serial
from serial.tools import list_ports
import tkinter as tk
import random

BAUDRATE = 9600

def find_virtual_port():
    for port in list_ports.comports():
        if 'com0com' in port.description:
            return port.device
    return None

def read_serial(ser):
    while True:
        data = ser.read(ser.in_waiting or 1)
        if data:
            print(data.decode('utf-8'), end='')
            
virtual_port = find_virtual_port()
if virtual_port:
    print(f"Connecting to virtual COM port: {virtual_port}")
    print(f"Baud rate: {BAUDRATE}")
    ser = serial.Serial(virtual_port, baudrate=BAUDRATE, timeout=1)
    thread = threading.Thread(target=read_serial, args=(ser,))
    thread.daemon = True
    thread.start()
    print("Connected. Waiting for data...")
else:
    print("No virtual COM port found.")

# Create the main window
window = tk.Tk()
window.title("RGB LED Matrix Emulator")

# Set the background color of the window
window.configure(bg="black")  # Set the desired background color

# Define the size of each square
square_size = 10

# Create a frame to hold the squares
frame = tk.Frame(window, bg="black")
frame.pack(padx=40, pady=40)  # Add padding around the frame

# Function to generate a random color
def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"#{r:02x}{g:02x}{b:02x}"

# Create a grid of colored squares
for i in range(36):
    for j in range(9):
        color = random_color()
        square = tk.Frame(frame, width=square_size, height=square_size, bg=color)
        square.grid(row=i, column=j, padx=2, pady=2)

# Create a label to display text at the bottom
text = "COM Port: " + virtual_port
label = tk.Label(window, text=text, bg="lightgray", fg="black")
label.pack(pady=10)  # Add padding below the label

# Start the main event loop
window.mainloop()