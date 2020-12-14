from struct import pack
import numpy as np
import math

HEIGHT = 600
WIDTH = 600

# приступаем к созданию файла
file = open('result.bmp', 'wb')
# необходимые для формата два заголовка на 14 и 40 байт и далее 8 байт цветовой карты(созданы два цвета-черный и белый)
file.write(b'BM')
file.write(pack('<LHHL', 62 + HEIGHT * WIDTH, 0, 0, 62))
file.write(pack('<LLLHHLLLLLL', 40, HEIGHT, WIDTH, 1, 8, 0, 0, 0, 0, 0, 0))
color_0 = (0, 0, 0, 0)
color_1 = (255, 255, 255, 0)
file.write(pack('<8B', *color_0, *color_1))

# создание параметрической функции
t = np.linspace(0, 2 * np.pi, 600)
x = 6 * np.cos(t) - 4 * (np.cos(t)) ** 3
y = 4 * (np.sin(t)) ** 3
# округляем значения
x = [round(v, 5) for v in x]
y = [round(v, 5) for v in y]

# создаем список пар [x,y]
all_pixels = []

for i in range(600):
    all_pixels.append([x[i], y[i]])
# сортируем у по возрастанию
y.sort()

# проходимся по у
for i in y:
    # создаем список для таких значений х которые подходят для у в рамках параметрической функции
    good_x = []
    for pair in all_pixels:
        if pair[1] == i:
            good_x.append(pair[0])
    # создаем список значений где числовое значение х приводим к номеру пикселя
    x_pixels = []
    for cur_y in good_x:
        x_pixels.append(math.trunc(cur_y * 106 + 300))
    # проходимся в ширину и красим пиксели выбранные ранее в черный, остальные в белый
    for a in range(WIDTH):
        if a in x_pixels:
            file.write(pack('<B', 0))
        else:
            file.write(pack('<B', 1))
file.close()
