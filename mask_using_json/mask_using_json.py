
import cv2
import numpy as np
import json
import os

# Значение яркости для конкретного класса
LABELS = {'price':255}

# Путь к папке с изображениями
img_path = "PATH"

# Путь к папке с JSON файлами
json_path = "PATH"

# Путь к папке для сохранения маски
save_path = "PATH"

# Создание папки для сохранения, если её не существует
if not os.path.exists(save_path):
    os.mkdir(save_path)

# Получение списка файлов в папке с изображениями
img_files = os.listdir(img_path)

# Обход каждого файла в папке с изображениями
for img_file in img_files:

    # Получение полного пути к файлу изображения
    img_full_path = os.path.join(img_path, img_file)

    # Чтение изображения с помощью OpenCV
    img = cv2.imread(img_full_path)

    # Получение имени файла без расширения
    img_name = os.path.splitext(img_file)[0]

    # Получение полного пути к файлу JSON
    json_full_path = os.path.join(json_path, img_name + ".json")

    # Чтение файла JSON
    with open(json_full_path) as f:
        json_data = json.load(f)

    # Обход каждого объекта в файле JSON
    for obj in json_data:
        mask = np.zeros_like(img)

        # Список для исключения ненужных классов
        values_to_remove = []
        obj = [ann for ann in obj['annotations'] if ann['label'] not in values_to_remove]
        if len(obj) != 0:
            for i in range(len(json_data[0]['annotations'])):

                # Определяем цвет для конкретного класса
                color = LABELS[obj[i]['label']]

                # Получение координат бокса
                x, y, h, w = obj[i]['coordinates']["x"], obj[i]['coordinates']["y"], obj[i]['coordinates']["height"], obj[i]['coordinates']["width"]

                # Вычисление координат верхнего левого угла и нижнего правого угла бокса
                x1, y1 = int(x - w / 2), int(y - h / 2)
                x2, y2 = int(x + w / 2), int(y + h / 2)

                # Создание черно-белой маски
                mask[y1:y2, x1:x2, :] = color

            # Сохранение маски в файл
            mask_name = img_name + ".png"
            mask_path = os.path.join(save_path, mask_name)
            cv2.imwrite(mask_path, mask)