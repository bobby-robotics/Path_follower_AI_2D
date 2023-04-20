"""
Klasse zur Linienerkennung.
Der Methode detect(img) muss ein RGB Bild übergeben werden.
Das Ergebnisbild wird als Binärbild zurückgegeben.

Diese Pakete müssen installiert sein:
    opencv-python
    numpy
    matplotlib
    scikit-image    (https://scikit-image.org/docs/stable/install.html)
"""

import cv2
import numpy as np
from skimage.morphology import skeletonize
import matplotlib.pyplot as plt


def detect(original_img):

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

    # Binäres Bild zurückgeben
    return new_img_2