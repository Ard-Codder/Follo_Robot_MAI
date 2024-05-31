import cv2
import numpy as np
from AlphaBot import AlphaBot
import torch
import yolov5.models as models
from yolov5.utils.general import non_max_suppression
from yolov5.utils.datasets import letterbox

# Инициализация робота
robot = AlphaBot()

# Инициализация камеры
cap = cv2.VideoCapture(0)

# Загрузка предобученной модели Yolo v5
model = models.yolov5s()
model.eval()
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = model.to(device)

# Определение коэффициентов для преобразования пикселей в углы поворота робота
x_coeff = 0.01
y_coeff = 0.01

# Определение класса, за которым будет следовать робот (в данном случае - мяч)
target_class = 0  # Индекс класса в наборе данных COCO

while True:
    # Получение кадра с камеры
    ret, frame = cap.read()

    # Преобразование кадра в формат, подходящий для модели Yolo v5
    img = letterbox(frame, new_shape=640)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0

    # Выполнение предсказания модели Yolo v5
    with torch.no_grad():
        pred = model(img)
        pred = non_max_suppression(pred, 0.4, 0.5)

    # Обработка результатов предсказания
    if len(pred) > 0:
        # Поиск объекта, соответствующего целевому классу
        target_obj = None
        for obj in pred[0]:
            if obj[5] == target_class:
                target_obj = obj
                break

        # Проверка, что объект был найден
        if target_obj is not None:
            # Вычисление центра массы объекта
            x_obj = int(target_obj[0] * frame.shape[1] + target_obj[2] * frame.shape[1] / 2)
            y_obj = int(target_obj[1] * frame.shape[0] + target_obj[3] * frame.shape[0] / 2)

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
