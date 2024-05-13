import RPi.GPIO as GPIO
import time

# Инициализация библиотеки RPi.GPIO
GPIO.setmode(GPIO.BCM)

# Настройка выводов GPIO для ультразвукового датчика расстояния
GPIO_TRIGGER = 16
GPIO_ECHO = 18

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# функция отправляет триггерный импульс и измеряет время, за которое
# импульс возвращается. Затем она рассчитывает расстояние на основе времени
# пролета импульса и скорости звука (343 м/с).
def measure_distance():
    # Отправка триггерного импульса
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # Измерение времени, за которое импульс возвращается
    start_time = time.time()
    stop_time = start_time

    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Расчет времени пролета импульса
    elapsed_time = stop_time - start_time

    # Расчет расстояния
    distance = elapsed_time * 34300 / 2

    return distance

# Измеряет расстояние каждые 0,5 секунды и выводит результат на экран
try:
    while True:
        distance = measure_distance()
        print("Distance: {:.2f} cm".format(distance))
        time.sleep(0.5)

except KeyboardInterrupt:
    # Очистка выводов GPIO при прерывании клавиатурой
    GPIO.cleanup()
