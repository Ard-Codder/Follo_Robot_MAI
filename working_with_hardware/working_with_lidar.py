import smbus
import time

# Адрес лидара в сети I2C
LIDAR_ADDRESS = 0x62

# Команды для лидара
COMMAND_START_MEASUREMENT = 0x04
COMMAND_STOP_MEASUREMENT = 0x00
COMMAND_GET_DISTANCE = 0x02

# Инициализация библиотеки smbus
bus = smbus.SMBus(1)

# Запуск измерения расстояния
bus.write_byte(LIDAR_ADDRESS, COMMAND_START_MEASUREMENT)

try:
    while True:
        # Получение расстояния
        bus.write_byte(LIDAR_ADDRESS, COMMAND_GET_DISTANCE)
        time.sleep(0.05)  # Задержка для стабилизации измерений
        distance = bus.read_word_data(LIDAR_ADDRESS, 0x04) / 10.0

        # Вывод расстояния на экран
        print("Distance: {:.2f} cm".format(distance))

        # Пауза между измерениями
        time.sleep(0.1)

except KeyboardInterrupt:
    # Остановка измерения расстояния и освобождение ресурсов при прерывании клавиатурой
    bus.write_byte(LIDAR_ADDRESS, COMMAND_STOP_MEASUREMENT)
    bus.close()
