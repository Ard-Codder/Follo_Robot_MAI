import time
import msvcrt
import os
import csv

file_path = '../server/drone_information.csv'


def write_data(data):
    try:
        with open('drone_information.csv', mode='w', newline='') as file:
            msvcrt.locking(file.fileno(), msvcrt.LK_LOCK, os.path.getsize(file_path))
            csv_writer = csv.writer(file)

            # Записываем данные в файл
            for row in data:
                csv_writer.writerow(row)

            print(f"Data '{data}' written to file.")
            msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, os.path.getsize(file_path))
    except Exception as e:
        print(f"Error writing data: {e}")


data = [
    ['id', 'name', 'charge_percentage'],
    ['1', 25, 25],
    ['2', 99, 99],
    ['3', 28, 28]
]

for i in range(10000000):
    write_data(data)
    time.sleep(0.5)
