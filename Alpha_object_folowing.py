import cv2
import numpy as np
from AlphaBot import AlphaBot

# Инициализация робота
robot = AlphaBot()

# Инициализация камеры
cap = cv2.VideoCapture(0)

# Определение цвета объекта, за которым будет следовать робот (в формате BGR)
target_color = np.array([230, 0, 0])

# Определение диапазона цветов вокруг целевого цвета
lower_bound = target_color - np.array([20, 20, 20])
upper_bound = target_color + np.array([20, 20, 20])

# Определение коэффициентов для преобразования пикселей в углы поворота робота
x_coeff = 0.01
y_coeff = 0.01

while True:
    # Получение кадра с камеры
    ret, frame = cap.read()

    # Преобразование кадра в пространство цветов HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Поиск пикселей на кадре, соответствующих целевому цвету
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Поиск контуров на маске
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Проверка, что хотя бы один контур был найден
    if len(contours) > 0:
        # Вычисление центра массы объекта
        M = cv2.moments(contours[0])
        x_obj = int(M['m10'] / M['m00'])
        y_obj = int(M['m01'] / M['m00'])

        # Вычисление углов поворота робота в зависимости от положения объекта
        x_angle = x_coeff * (x_obj - frame.shape[1] / 2)
        y_angle = y_coeff * (y_obj - frame.shape[0] / 2)

        # Управление движением робота
        if x_angle > 0:
            robot.right()
        elif x_angle < 0:
            robot.left()
        else:
            if y_angle > 0:
                robot.backward()
            elif y_angle < 0:
                robot.forward()
            else:
                robot.stop()
    else:
        robot.stop()

    # Вывод кадра на экран
    cv2.imshow('frame', frame)

    # Проверка нажатия клавиши 'q' для выхода из цикла
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Очистка ресурсов
cap.release()
cv2.destroyAllWindows()
