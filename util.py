import RPi.GPIO as GPIO

GPIO.setwarnings(False)

edgetpu = 0  # Если подключен ускоритель Coral USB, то установите '1', иначе '0'

m1_1 = 12
m1_2 = 13
m2_1 = 20
m2_2 = 21

cam_light = 17
headlight_right = 18
headlight_left = 27
sp_light = 9


def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(m1_1, GPIO.OUT)
    GPIO.setup(m1_2, GPIO.OUT)
    GPIO.setup(m2_1, GPIO.OUT)
    GPIO.setup(m2_2, GPIO.OUT)
    GPIO.setup(cam_light, GPIO.OUT)
    GPIO.setup(headlight_right, GPIO.OUT)
    GPIO.setup(headlight_left, GPIO.OUT)
    GPIO.setup(sp_light, GPIO.OUT)


def back():
    print("move back")
    GPIO.output(m1_1, False)
    GPIO.output(m1_2, True)
    GPIO.output(m2_1, True)
    GPIO.output(m2_2, False)


def right():
    GPIO.output(m1_1, True)
    GPIO.output(m1_2, False)
    GPIO.output(m2_1, True)
    GPIO.output(m2_2, False)


def left():
    GPIO.output(m1_1, False)
    GPIO.output(m1_2, True)
    GPIO.output(m2_1, False)
    GPIO.output(m2_2, True)


def forward():
    GPIO.output(m1_1, True)
    GPIO.output(m1_2, False)
    GPIO.output(m2_1, False)
    GPIO.output(m2_2, True)


def stop():
    GPIO.output(m1_1, False)
    GPIO.output(m1_2, False)
    GPIO.output(m2_1, False)
    GPIO.output(m2_2, False)


def head_lights(state):
    if state == "ON":
        GPIO.output(headlight_left, True)
        GPIO.output(headlight_right, True)
    # print("light on")
    else:
        GPIO.output(headlight_left, False)
        GPIO.output(headlight_right, False)
    # print("light off")


def red_light(state):
    if state == "ON":
        GPIO.output(sp_light, True)
    # print("light on")
    else:
        GPIO.output(sp_light, False)
    # print("light off")
