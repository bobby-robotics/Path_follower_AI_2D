import Line
import cv2
import os
from cv2 import WINDOW_NORMAL
import numpy as np

START_X_COORDINATE = 20
points = []
list = []

img = cv2.imread(os.path.abspath('IMG/line1.jpg'))
if img is None:
    print('Fehler: Bild konte nicht eingelesen werden. Eventuell falscher Pfad oder Dateiname.')
    exit()

line = Line.detect(img)
height, width = line.shape

print('STATUS: line detection done')


# Startpunkt finden (Spalte gegeben)
count = 0
for y in range(height):
    if line[y][START_X_COORDINATE] == 1:
        points.append((START_X_COORDINATE, y))
        count += 1
if count != 1:
    print('ERROR: No starting point found.')
    print(count)
    exit()

print('STATUS: get start point done')


# Alle Punkte der Linie in ein Array speichern
for x in range(width):
    if x < START_X_COORDINATE:
        continue
    for y in range(height):
        if line[y][x] == 1:
            list.append([x, y, 0]);

print('STATUS: list points done')



# Punkte sortieren
while(len(list) > 0):
    for index in range(len(list)):
        list[index][2] = (points[-1][0]-list[index][0])**2 + (points[-1][1]-list[index][1])**2

    def sortKey(val):
        return val[2]
    list.sort(key=sortKey)

    points.append((list[0][0], list[0][1]))
    list.pop(0)

print('STATUS: sort points done')


# Ergebnis anzeigen
window_size = (1200, 900)

cv2.namedWindow('Line', WINDOW_NORMAL)
cv2.resizeWindow('Line', window_size[0], window_size[1])

new_img = np.zeros(line.shape, dtype="uint8")

for point in points:
    new_img[point[1]][point[0]] = 255
    cv2.imshow('Line', new_img)
    k = cv2.waitKey(3) & 0xFF
    if k == ord('q'):               # Taste q zum schließen
        cv2.destroyAllWindows()
        break
