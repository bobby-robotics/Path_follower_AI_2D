"""
Beispiel zum erkennen der Linie aus einem realen, aufgenommenen Bild.

Diese Pakete müssen installiert sein:
    opencv-python
    numpy
    matplotlib
    scikit-image    (https://scikit-image.org/docs/stable/install.html)
"""

from cv2 import WINDOW_NORMAL
import cv2
import numpy as np
from skimage.morphology import skeletonize
import matplotlib.pyplot as plt
import os


# Bild einlesen
original_img = cv2.imread(os.path.abspath('IMG/line1.jpg'))
if original_img is None:
    print('Fehler: Bild konte nicht eingelesen werden. Eventuell falscher Pfad oder Dateiname.')
    exit()

# Bild in Gray-Bild umwandeln
img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

# Schwellwert anwenden
img = cv2.medianBlur(img, 3)
img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 2)

# Konturen im Bild finden
contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Nach der größten Kontur filtern und diese auf ein schwarzes Bild übertragen
img_line = np.zeros(img.shape, dtype="uint8")
line = max(contours, key=cv2.contourArea)
cv2.drawContours(img_line, [line], -1, 255, 5)

# Skeletonize-Methode anwenden um die Linie auf einen Pixel Breite zu reduzieren
new_img = skeletonize(img_line)

# Ergebnis in ein binäres Bild übertragen
new_img_2 = np.zeros(img.shape, dtype="uint8")
r, c = new_img.shape
for row in range(r):
    for column in range(c):
        if new_img[row][column] == True:
            new_img_2[row][column] = 1


# Ergebnis anzeigen
# (dieser Schritt dient nur der Visualisierung und hat nichts mit der Bildverarbeitung zu tun)

window_size = (1600, 600)    # Fenstergröße zum anzeigen

cv2.namedWindow('Ergebnis', WINDOW_NORMAL)
cv2.resizeWindow('Ergebnis', window_size[0], window_size[1])

text = 'q = quit/close; s = save'
original_img = cv2.putText(original_img, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA, False)
ergebnis = np.concatenate((original_img, cv2.cvtColor(new_img_2*255, cv2.COLOR_GRAY2BGR)), axis=1)
cv2.imshow('Ergebnis', ergebnis)

while True:
    k = cv2.waitKey(0) & 0xFF
    if k == ord('q'):               # Taste q zum schließen
        cv2.destroyAllWindows()
        break
    if k == ord('s'):               # Taste s um Ergebnis abzuspeichern
        cv2.imwrite('thinned.jpg', new_img_2*255)


# Alle Fenster schließen
cv2.destroyAllWindows()