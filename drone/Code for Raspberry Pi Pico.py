from machine import UART, Pin
import time

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

def send_message(message):
    uart.write(message)

def main():
    counter = 0
    while True:
        message = f"Hello from Raspberry Pi Pico! Counter: {counter}\n"
        send_message(message)
        time.sleep(1)
        counter += 1

if __name__ == "__main__":
    main()
