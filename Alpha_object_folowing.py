import cv2
import numpy as np
from AlphaBot import AlphaBot
import common as cm
from util import edgetpu

# Инициализация робота
robot = AlphaBot()

# Инициализация камеры
cap = cv2.VideoCapture(0)

# Определение списка допустимых объектов для отслеживания
arr_valid_objects = ['apple', 'person', 'dog', 'cat', 'car']

# Загрузка модели TF Lite и меток для классов
model_dir = 'Models'
model = 'mobilenet_ssd_v2_coco_quant_postprocess.tflite'
model_edgetpu = 'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite'
lbl = 'coco_labels.txt'
interpreter, labels = cm.load_model(model_dir, model if edgetpu == 0 else model_edgetpu, lbl, edgetpu)

# Определение глобальных переменных для отслеживания объекта
x_deviation = 0
y_deviation = 0
arr_track_data = [0, 0, 0, 0, 0, 0]
tolerance = 0.1

# Определение коэффициентов для преобразования пикселей в углы поворота робота
x_coeff = 0.01
y_coeff = 0.01

def stop():
    robot.stop()

def track_object(objs, labels):
    global x_deviation, y_deviation, tolerance, arr_track_data

    if len(objs) == 0:
        print("no objects to track")
        stop()
        arr_track_data = [0, 0, 0, 0, 0, 0]
        return

    k = 0
    flag = 0
    for obj in objs:
        lbl = labels.get(obj.id, obj.id)
        k = arr_valid_objects.count(lbl)
        if k > 0:
            x_min, y_min, x_max, y_max = list(obj.bbox)
            flag = 1
            break

    if flag == 0:
        print("selected object no present")
        return

    x_diff = x_max - x_min
    y_diff = y_max - y_min
    print("x_diff: ", round(x_diff, 5))
    print("y_diff: ", round(y_diff, 5))

    obj_x_center = x_min + (x_diff / 2)
    obj_x_center = round(obj_x_center, 3)

    obj_y_center = y_min + (y_diff / 2)
    obj_y_center = round(obj_y_center, 3)

    x_deviation = round(0.5 - obj_x_center, 3)
    y_deviation = round(0.5 - obj_y_center, 3)

    print("{", x_deviation, y_deviation, "}")

    thread = Thread(target=move_robot)
    thread.start()

    arr_track_data[0] = obj_x_center
    arr_track_data[1] = obj_y_center
    arr_track_data[2] = x_deviation
    arr_track_data[3] = y_deviation

def move_robot():
    global x_deviation, y_deviation, tolerance, arr_track_data

    print("Moving robot")
    print(x_deviation, y_deviation, tolerance, arr_track_data)

    if abs(x_deviation) < tolerance and abs(y_deviation) < tolerance:
        cmd = "Stop"
        delay1 = 0
        stop()

    else:
        if abs(x_deviation) > abs(y_deviation):
            if x_deviation >= tolerance:
                cmd = "Move Left"
                delay1 = get_delay(x_deviation, 'l')
                robot.left(delay1)

            if x_deviation <= -1 * tolerance:
                cmd = "Move Right"
                delay1 = get_delay(x_deviation, 'r')
                robot.right(delay1)
        else:
            if y_deviation >= tolerance:
                cmd = "Move Forward"
                delay1 = get_delay(y_deviation, 'f')
                robot.forward(delay1)

            if y_deviation <= -1 * tolerance:
                cmd = "Move Backward"
                delay1 = get_delay(y_deviation, 'b')
                robot.backward(delay1)

    arr_track_data[4] = cmd
    arr_track_data[5] = delay1

def get_delay(deviation, direction):
    deviation = abs(deviation)
    if direction == 'f' or direction == 'b':
        if deviation >= 0.3:
            d = 0.1
        elif 0.2 <= deviation < 0.30:
            d = 0.075
        elif 0.15 <= deviation < 0.2:
            d = 0.045
        else:
            d = 0.035
    else:
        if deviation >= 0.4:
            d = 0.080
        elif 0.35 <= deviation < 0.40:
            d = 0.070
        elif 0.30 <= deviation < 0.35:
            d = 0.060
        elif 0.25 <= deviation < 0.30:
            d = 0.050
        elif 0.20 <= deviation < 0.25:
            d = 0.040
        else:
            d = 0.030

    return d

def draw_overlays(cv2_im, objs, labels, arr_dur, arr_track_data):
    # Получение размеров изображения
    height, width, channels = cv2_im.shape

    # Установка шрифта для вывода текста
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Определение глобальной переменной для допустимого отклонения
    global tolerance

    # Рисование черного прямоугольника в верхней части изображения для выделения текстовой информации
    cv2_im = cv2.rectangle(cv2_im, (0, 0), (width, 24), (0, 0, 0), -1)

    # Вычисление времени, затраченного на обработку изображения, обнаружение объектов и другие операции
    cam = round(arr_dur[0] * 1000, 0)
    inference = round(arr_dur[1] * 1000, 0)
    other = round(arr_dur[2] * 1000, 0)
    text_dur = 'Camera: {}ms   Inference: {}ms   other: {}ms'.format(cam, inference, other)

    # Вывод текстовой информации о времени обработки на изображении
    cv2_im = cv2.putText(cv2_im, text_dur, (int(width / 4) - 30, 16), font, 0.4, (255, 255, 255), 1)

    # Вычисление текущей частоты кадров (FPS) и вывод ее на изображении
    total_duration = cam + inference + other
    fps = round(1000 / total_duration, 1)
    text1 = 'FPS: {}'.format(fps)
    cv2_im = cv2.putText(cv2_im, text1, (10, 20), font, 0.7, (150, 150, 255), 2)

    # Рисование черного прямоугольника в нижней части изображения для выделения элементов управления
    cv2_im = cv2.rectangle(cv2_im, (0, height - 24), (width, height), (0, 0, 0), -1)

    # Вывод текстовой информации о текущем отклонении объекта от центра изображения по осям X и Y
    # и допустимом отклонении, цвет текста зависит от превышения допустимого отклонения
    str_tol = 'Tol : {}'.format(tolerance)
    cv2_im = cv2.putText(cv2_im, str_tol, (10, height - 8), font, 0.55, (150, 150, 255), 2)

    x_dev = arr_track_data[2]
    str_x = 'X: {}'.format(x_dev)
    if abs(x_dev) < tolerance:
        color_x = (0, 255, 0)
    else:
        color_x = (0, 0, 255)
    cv2_im = cv2.putText(cv2_im, str_x, (110, height - 8), font, 0.55, color_x, 2)

    y_dev = arr_track_data[3]
    str_y = 'Y: {}'.format(y_dev)
    if abs(y_dev) < tolerance:
        color_y = (0, 255, 0)
    else:
        color_y = (0, 0, 255)
    cv2_im = cv2.putText(cv2_im, str_y, (220, height - 8), font, 0.55, color_y, 2)

    # Вывод текстовой информации о текущей команде управления, скорости и статусе отслеживания объекта
    cmd = arr_track_data[4]
    cv2_im = cv2.putText(cv2_im, str(cmd), (int(width / 2) + 10, height - 8), font, 0.68, (0, 255, 255), 2)

    delay1 = arr_track_data[5]
    str_sp = 'Speed: {}%'.format(round(delay1 / (0.1) * 100, 1))
    cv2_im = cv2.putText(cv2_im, str_sp, (int(width / 2) + 185, height - 8), font, 0.55, (150, 150, 255), 2)

    if cmd == 0:
        str1 = "No object"
    elif cmd == 'Stop':
        str1 = 'Acquired'
    else:
        str1 = 'Tracking'
    cv2_im = cv2.putText(cv2_im, str1, (width - 140, 18), font, 0.7, (0, 255, 255), 2)

    # Рисование перекрещивающихся линий в центре изображения для облегчения визуального определения центра
    cv2_im = cv2.rectangle(cv2_im, (0, int(height / 2) - 1), (width, int(height / 2) + 1), (255, 0, 0), -1)
    cv2_im = cv2.rectangle(cv2_im, (int(width / 2) - 1, 0), (int(width / 2) + 1, height), (255, 0, 0), -1)

    # Рисование красной точки в центре обнаруженного объекта
    cv2_im = cv2.circle(cv2_im, (int(arr_track_data[0] * width), int(arr_track_data[1] * height)), 7, (0, 0, 255), -1)

    # Рисование зеленого прямоугольника вокруг допустимой зоны отслеживания объекта
    cv2_im = cv2.rectangle(cv2_im, (int(width / 2 - tolerance * width), int(height / 2 - tolerance * height)),
                           (int(width / 2 + tolerance * width), int(height / 2 + tolerance * height)), (0, 255, 0), 2)

    # Рисование прямоугольников вокруг обнаруженных объектов и вывод текстовой информации о проценте уверенности
    # в обнаружении и метке объекта, цвет текста и прямоугольника зависит от метки объекта
    for obj in objs:
        x0, y0, x1, y1 = list(obj.bbox)
        x0, y0, x1, y1 = int(x0 * width), int(y0 * height), int(x1 * width), int(y1 * height)
        percent = int(100 * obj.score)

        box_color, text_color, thickness = (0, 150, 255), (0, 255, 0), 2
        cv2_im = cv2.rectangle(cv2_im, (x0, y0), (x1, y1), box_color, thickness)

        # text3 = '{}% {}'.format(percent, labels.get(obj.id, obj.id))
        # cv2_im = cv2.putText(cv2_im, text3, (x0, y1-5),font, 0.5, text_color, thickness)

    return cv2_im

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
            robot.right(x_angle)
        elif x_angle < 0:
            robot.left(abs(x_angle))
        else:
            if y_angle > 0:
                robot.backward(y_angle)
            elif y_angle < 0:
                robot.forward(abs(y_angle))
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
