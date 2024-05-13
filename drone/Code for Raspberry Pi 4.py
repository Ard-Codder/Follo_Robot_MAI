import time
import serial

ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)

def receive_message():
    return ser.readline().decode('utf-8').rstrip()

def main():
    while True:
        message = receive_message()
        print(message)

if __name__ == "__main__":
    main()
