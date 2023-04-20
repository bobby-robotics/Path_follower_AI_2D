import Line
import cv2
import os
from cv2 import WINDOW_NORMAL
import numpy as np
#import enum_motion
#from enum_motion import Moutions


def find_direction(delta_x, delta_y):

    UP = "u"    
    DOWN = "d"
    LEFT = "l"
    RIGHT = "r"
    CLOCKWISE = "cw"
    COUNTERCLOCKWISE = "ccw"

    path = []

    print(delta_x,delta_y)

    if delta_x < 0:
        path.append( LEFT)
    
    elif delta_x > 0:
        path.append( RIGHT)

    if delta_y < 0:
        path.append( UP)

    elif delta_y > 0:
        path.append( DOWN)

    if delta_x*delta_y != 0:

        if  LEFT in path: 
            if  DOWN in path:
                path.append( COUNTERCLOCKWISE)
            elif  UP in path:
                path.append( CLOCKWISE)
        elif  RIGHT in path:
            if  UP in path:
                path.append( COUNTERCLOCKWISE)
            elif  DOWN in path:
                path.append( CLOCKWISE)

    return ','.join(path)


START_X_COORDINATE = 20     # An dieser x-Koordinate wird der Startpunkt der Linie gesetzt
STATE_DIMENSION = 7         # n*n*1 Array Bsp: 5x5 od 7x7 oder 9x9
points = []                 # Liste mit Pixelkoordinaten der Linie (sortiert von Anfang bis Ende der Linie): points = [(x1, y1), (x2, y2), ... , (xn, yn)]
list = []                   # Nur für temporäre Verarbeitungsschritte notwendig
states = []                 # States ist eine Liste mit Binären Bildern mit der Auflösung n*n wobei n = STATE_DIMENSION entspricht

img = cv2.imread(os.path.abspath('Bildverarbeitung/IMG/line1.jpg'))
if img is None:
    print('Fehler: Bild konte nicht eingelesen werden. Eventuell falscher Pfad oder Dateiname.')
    exit()


# Erkennen der Linie. Gibt binäres Bild zurück.
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

# States abgreifen
for point in points:
    y1 = point[1] - int(STATE_DIMENSION/2)
    y2 = point[1] + int(STATE_DIMENSION/2) +1
    x1 = point[0] - int(STATE_DIMENSION/2)
    x2 = point[0] + int(STATE_DIMENSION/2) +1
    states.append(line[y1:y2, x1:x2])



# Ergebnis anzeigen nur zur Visualisierung hat nichts mit der Bildverarbeitung zu tun

window_size = (500, 500)
cv2.namedWindow('States', WINDOW_NORMAL)
cv2.resizeWindow('States', window_size[0], window_size[1])

window_size = (1200, 900)
cv2.namedWindow('Line', WINDOW_NORMAL)
cv2.resizeWindow('Line', window_size[0], window_size[1])

line_bgr = line*255
line_bgr = cv2.cvtColor(line_bgr, cv2.COLOR_GRAY2BGR)

cv2.moveWindow('States', 80, 40)
cv2.moveWindow('Line', 600, 40)

text = "press 's' to start"
img = cv2.putText(img, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA, False)
cv2.imshow('Line', img)

while(1):
    k = cv2.waitKey(0) & 0xFF
    if k == ord('s'):
        break

path = []
last_point = None

for i in range(len(states)):


    if last_point is not None:

        delta_x = points[i][0] - last_point[0] 
        delta_y = points[i][1] - last_point[1] 

        path.append(find_direction(delta_x, delta_y))

    line_bgr[points[i][1]][points[i][0]] = (0, 0, 255)
    cv2.imshow('Line', line_bgr)
    cv2.imshow('States', states[i]*255)
    k = cv2.waitKey(20) & 0xFF
    if k == ord('q'):               # Taste q zum schließen
        cv2.destroyAllWindows()
        break

    last_point = [ points[i][0], points[i][1]  ]

print(','.join(path))


cv2.destroyAllWindows()