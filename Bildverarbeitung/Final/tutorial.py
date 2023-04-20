"""
Beispiele zur Nutzung der Klasse Line.

Diese Pakete müssen installiert sein:
    opencv-python
    numpy
    scikit-image    (https://scikit-image.org/docs/stable/install.html)
"""

import Line
import cv2
import os


########################
# 1) Ein Bild einlesen.#
########################

img = cv2.imread(os.path.abspath('IMG/line1.jpg'))
if img is None:
    print('Error: file could not be found or read.')
    exit()


#############################################################
#                                                           #
# 2) Biild übergeben und zwei Listen zurückbekommen.        #
#                                                           #
#    Liste1 enthält Pixelkoordinaten der Linienpunkte,      #
#    Liste2 enthält alle States der jeweiligen Punkte       #
#                                                           #
#    Übergabeparameter:                                     #
#                                                           #
#       img = aufgenommenes RGB-Bild ODER                   #
#             generiertes binäres Bild                      #
#                                                           #
#       START_X_COORDINATE = Bildspalte, bzw. x-Koordinate  #
#             an der die Linie anfängt (alle Spalten        #
#             links davon werden ignoriert, der y-Abschnitt #
#             wird automatisch bestimmt.                    #
#                                                           #
#       STATE_DIMENSION = n*n-Dimension der States          #
#             (Bsp.: 5 steht für 5x5)                       #
#                                                           #
#############################################################

points, states = Line.states(img, 20, 5)


########################################################
#                                                      #
# 3) Visuelle Ausgabe der States und Points            #
#    (dient nur zu Demonstrationszwecken)              #
#                                                      #
#    Übergabeparameter:                                #
#                                                      #
#       img = aufgenommenes RGB-Bild ODER              #
#             generiertes binäres Bild                 #
#                                                      #
#       points = Liste an Punktkoordinaten             #
#                                                      #
#       states = Liste an States                       #
#                                                      #
#       scale=1 (optional) damit kann die Fenstergröße #
#               für die Ausgabe verändert werden.      #
#               (  1  = 100% entspricht 900x1800,      #
#                 0.8 =  80% wäre eine Verkleinerung,  #
#                 1.2 = 120% wäre eine Vergrößerung )  #
#                                                      #
########################################################

Line.show(img, points, states, scale=0.8)


######################################################################
#                                                                    #
# 4) Line.detect()-Methode                                           #
#                                                                    #
# Dieser Methode kann ein aufgenommenes RGB-Bild übergeben werden.   #
# Zurückgegeben wird ein binäres Bild mit der erkannten Linie.       #
# (identisch wie die generierten Testbilder)                         #
#                                                                    #
# Diese Methode wird automatisch in der Line.states()-Methode        #
# aufgerufen, und wird daher nicht eigenständig benötigt.            #
#                                                                    #
# Wird ein, mit dieser Methode oder anderweitig generiertes Testbild #
# der Methode Line.states() übergeben, wird in dieser die detect()-  #
# Methode nicht nochmal aufgerufen.                                  #
#                                                                    #
######################################################################

# img = Line.detect(img)
# points, states = Line.states(img, 20, 5)
# Line.show(img, points, states, scale=0.8)


########################################
# 5) Terminalausgabe points und states #
########################################

# print(points)       # alle ausgeben                    
# print(states)       # alle ausgeben

print('point=', points[0])      # einen ausgeben             
print('state=\n', states[0])      # einen ausgeben