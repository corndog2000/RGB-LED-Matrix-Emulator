import sys
import threading
import serial
from serial.tools import list_ports

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

if __name__ == '__main__':
    virtual_port = find_virtual_port()
    if virtual_port:
        print(f"Connecting to virtual COM port: {virtual_port}")
        ser = serial.Serial(virtual_port, baudrate=9600, timeout=1)
        thread = threading.Thread(target=read_serial, args=(ser,))
        thread.daemon = True
        thread.start()
        print("Connected. Waiting for data...")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\nDisconnecting...")
            ser.close()
    else:
        print("No virtual COM port found.")