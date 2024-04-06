from ctypes import sizeof
import sys
import threading
import serial
from serial.tools import list_ports
import tkinter as tk
import random

# Connect to a virtual com port created by com0com.
# https://com0com.sourceforge.net/

BAUDRATE = 115200

def find_virtual_port():
    for port in list_ports.comports():
        if 'com0com' in port.description:
            return port.device
    return None

def read_serial(ser):
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().rstrip()
            split_line = line.split()
            # Convert each hex byte string to an integer
            line_ints = [int(byte, 16) for byte in split_line]
            
            if line:
                print(line_ints)
                
                if len(split_line) % 5 == 0:
                    print("Good serial data")
                    
                    for idx in range(0, len(split_line), 5):
                        grid_pos = (line_ints[idx] << 8) + line_ints[idx+1]
                        red = line_ints[idx + 2]
                        green = line_ints[idx + 3]
                        blue = line_ints[idx + 4]
                        
                        new_color = f"#{red:02x}{green:02x}{blue:02x}"
                        
                        squares[grid_pos].configure(bg=new_color)
            
virtual_port = find_virtual_port()
if virtual_port:
    print(f"Connecting to virtual COM port: {virtual_port}")
    print(f"Baud rate: {BAUDRATE}")
    ser = serial.Serial(virtual_port, baudrate=BAUDRATE, timeout=0.01)
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

# Allow the window to be dragged to be resized
window.resizable(True, True)

# Define the size of each square
square_size = 15

# Create a frame to hold the squares
frame = tk.Frame(window, bg="black")
frame.pack(padx=40, pady=40)  # Add padding around the frame

# Create a list to store the square frames
squares = []

# Function to generate a random color
def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"#{r:02x}{g:02x}{b:02x}"

# Create a grid of colored squares
for i in range(32):
    for j in range(9):
        color = random_color()
        square = tk.Frame(frame, width=square_size, height=square_size, bg=color)
        square.grid(row=i, column=j, padx=2, pady=2)
        squares.append(square)

# Function to set all squares to red
def set_black():
    for square in squares:
        square.configure(bg="black")

# Create a label to display text at the bottom
text = f"COM Port: {virtual_port}"
label = tk.Label(window, text=text, bg="black", fg="white")
label.pack(pady=10)  # Add padding below the label

# Create a button to set all squares to red
button = tk.Button(window, text="Set Black", command=set_black)
button.pack(pady=10)  # Add padding below the button

# Start the main event loop
window.mainloop()