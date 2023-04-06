""" 
Dieses Python-Skript wandelt eine lückenhafte Linie in 
eine durchgehende Linie um, die wieder ein Pixel breit ist.

Installation des "scikit-image" notwendig für die skeletonize-
Methode (z.B. mit "pip3 install scikit-image")
"""

from cv2 import WINDOW_NORMAL
import cv2
import numpy as np
from skimage.morphology import skeletonize


# Methode zum umwandeln eines Gray Bildes in ein binäres Bild
def gray2binary(img):
    height, width = img.shape
    for row in range(height):
        for column in range(width):
            if img[row][column] < 128:
                img[row][column] = 0
            else:
                img[row][column] = 1
    return img

# Methode zum umwandeln einer 2dMatrix mit True/False Werten in ein binäres Bild
# Notwendig, da die skeletonize-Methode ein Array mit Boolean Werten zurückgibt
def boolean2binary(array):
    img = np.zeros(array.shape, dtype="uint8")
    height, width = img.shape
    for row in range(height):
        for column in range(width):
            if array[row][column] == True:
                img[row][column] = 1
    return img


# Bild einlesen
img = cv2.imread('generated_images/2023-04-04_18_20_23.jpeg')

# RGB- in Gray-Bild umwandeln
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Gray-Bild zu Binär-Bild umwandeln
img = gray2binary(img)

# Linie breiter machen um Lücken zu füllen
kernel = np.ones((5,5), np.uint8)
img = cv2.dilate(img, kernel, iterations=1)

# Linie auf einen Pixel Breite reduzieren
array = skeletonize(img)

# Boolean-Array in Gray-Bild umwandeln
img = boolean2binary(array)

# Bild anzeigen
cv2.imshow('image', img*255)
cv2.waitKey(0)
cv2.destroyAllWindows()