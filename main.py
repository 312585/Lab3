from struct import pack
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# создание параметрической функции
t = np.linspace(0, 2 * np.pi)
x = 6 * np.cos(t) - 4 * (np.cos(t)) ** 3
y = 4 * (np.sin(t)) ** 3

# Создание и сохранение графика в файл
fig = plt.figure(figsize=(4, 4))
plt.plot(x, y, 'k')
plt.savefig('plot.png')

# открываем файл при помощи библиотеки для удобства,
# поворачиваем так как изображение открывается повернутым на 90 градусов
img = Image.open('plot.png').rotate(-90)
# получаем необходимые данные
width, height = img.size
pixels = img.load()

# на основании загруженного файла получаем данные для нового файла
new_pixels = []
for x in range(width):
    for y in range(height):
        pix = pixels[x, y]
        one_pixel = 1 if round(sum(pix)/float(len(pix))) > 127 else 0
        new_pixels.append(one_pixel)
img.close()

# приступаем к созданию файла
file = open('result.bmp', 'wb')
# необходимые для формата два заголовка на 14 и 40 байт и далее 8 байт цветовой карты(созданы два цвета-черный и белый)
file.write(b'BM')
file.write(pack('<LHHL', 62 + width * height, 0, 0, 62))
file.write(pack('<LLLHHLLLLLL', 40, width, height, 1, 8, 0, 0, 0, 0, 0, 0))
color_0 = (0, 0, 0, 0)
color_1 = (255, 255, 255, 0)
file.write(pack('<8B', *color_0, *color_1))
# пишем данные в файл
file.write(pack(f'<{len(new_pixels)}B', *new_pixels))
file.close()
