import RPi.GPIO as GPIO
import time

# Инициализация библиотеки RPi.GPIO
GPIO.setmode(GPIO.BCM)

# Настройка вывода GPIO для управления сервоприводом
servo_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)

# Настройка ШИМ (PWM) на выводе GPIO
pwm = GPIO.PWM(servo_pin, 50)  # Частота 50 Гц
pwm.start(2.5)  # Начальная ширина импульса 2,5% (соответствует углу поворота 90 градусов)

try:
    # Поворот сервопривода на 0 градусов
    duty_cycle = 2.5 / 180 * 0 + 2.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)

    # Поворот сервопривода на 90 градусов
    duty_cycle = 2.5 / 180 * 90 + 2.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)

    # Поворот сервопривода на 180 градусов
    duty_cycle = 2.5 / 180 * 180 + 2.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)

except KeyboardInterrupt:
    # Остановка ШИМ (PWM) и сброс вывода GPIO в исходное состояние при прерывании клавиатурой
    pwm.stop()
    GPIO.cleanup()
