import yolov5
import cv2
import numpy as np
from AlphaBot import AlphaBot
import torch
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression
from yolov5.utils.augmentations import letterbox

# Инициализация робота
robot = AlphaBot()

# Инициализация камеры
cap = cv2.VideoCapture(0)

# Определение устройства для вычислений
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# Загрузка предобученной модели YOLOv5n
model_path = 'yolov5n.pt'  # Укажите путь к файлу модели
model = attempt_load(model_path)
model.to(device)
model.eval()

# Определение коэффициентов для преобразования пикселей в углы поворота робота
x_coeff = 0.01
y_coeff = 0.01

# Определение целевого класса для отслеживания (в данном случае - мяч)
target_class = 0  # Индекс класса в наборе данных COCO

# Ограничение частоты кадров до 10 кадров в секунду
fps = 10
wait_time = int(1000 / fps)

while True:
    # Получение кадра с камеры
    ret, frame = cap.read()

    # Преобразование кадра в формат, подходящий для модели YOLOv5n
    img = letterbox(frame, new_shape=640)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).unsqueeze(0).to(device)
    img = img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0

    # Выполнение детектирования модели YOLOv5n
    with torch.no_grad():
        pred = model(img)
        pred = non_max_suppression(pred, 0.4, 0.5)

    # Обработка результатов детектирования
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

            # Вывод информации об объекте на экран
            cv2.putText(frame, f'{target_class}: {target_obj[4]:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x_obj - 10, y_obj - 10), (x_obj + 10, y_obj + 10), (0, 255, 0), 2)

            # Вывод информации об объекте в консоль
            print(f'Object {target_class} detected with confidence {target_obj[4]:.2f} at '
                  f'coordinates ({x_obj}, {y_obj})')

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

    # Ожидание нажатия клавиши
    key = cv2.waitKey(wait_time)

    # Прекращение работы программы при нажатии клавиши 'q'
    if key == ord('q'):
        break

# Очистка ресурсов
cap.release()
cv2.destroyAllWindows()