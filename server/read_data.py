import time
import msvcrt
import os
import csv

file_path = '../server/drone_information.csv'

def read_data():
    try:
        with open('drone_information.csv', mode='r') as file:
            msvcrt.locking(file.fileno(), msvcrt.LK_LOCK, os.path.getsize(file_path))
            csv_reader = csv.reader(file)
            # Читаем данные из файла
            for data in csv_reader:
                print(data)  # Выводим каждую строку

            print(f"Data read from file: {data}")
            msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, os.path.getsize(file_path))
    except Exception as e:
        print(f"Error reading data: {e}")


for i in range(100000):
    read_data()
    time.sleep(0.5)
