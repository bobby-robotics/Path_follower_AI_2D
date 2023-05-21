"""
Bildverarbeitung KI:

Diese Pakete müssen installiert sein:
    opencv-python
    numpy
    scikit-image    (https://scikit-image.org/docs/stable/install.html)
"""

import cv2
import numpy as np
from skimage.morphology import skeletonize
from cv2 import WINDOW_NORMAL


class Line():

    @staticmethod
    def find_direction(delta_x, delta_y):

        UP = "u"    
        DOWN = "d"
        LEFT = "l"
        RIGHT = "r"
        CLOCKWISE = "cw"
        COUNTERCLOCKWISE = "ccw"

        path = []

        #print(delta_x,delta_y)

        if delta_x < 0:
            path.append( LEFT)
        
        elif delta_x > 0:
            path.append( RIGHT)

        if delta_y < 0:
            path.append( UP)

        elif delta_y > 0:
            path.append( DOWN)

        # if delta_x*delta_y != 0:

        #     if  LEFT in path: 
        #         if  DOWN in path:
        #             path.append( COUNTERCLOCKWISE)
        #         elif  UP in path:
        #             path.append( CLOCKWISE)
        #     elif  RIGHT in path:
        #         if  UP in path:
        #             path.append( COUNTERCLOCKWISE)
        #         elif  DOWN in path:
        #             path.append( CLOCKWISE)

        return ','.join(path)

    @staticmethod
    def detect(original_img, generated = False):


        # Bild in Gray-Bild umwandeln
        img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

        

        if generated:
            pass
        else:
            # Schwellwert anwenden
            img = cv2.medianBlur(img, 3)
            img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 2)

        height,width = img.shape

        # cut the top part of the img
        img[ : 100, :width] = 0
        
        # Konturen im Bild finden
        contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

       

        # Nach der größten Kontur filtern und diese auf ein schwarzes Bild übertragen
        img_line = np.zeros(img.shape, dtype="uint8")
        line = max(contours, key=cv2.contourArea)
        cv2.drawContours(img_line, [line], -1, 255, 5)
        
        # Skeletonize-Methode anwenden um die Linie auf einen Pixel Breite zu reduzieren
        new_img = skeletonize(img_line)

        # cv2.imshow("",new_img.astype(np.uint8)*255)
        # cv2.waitKey(0)

        # Ergebnis in ein binäres Bild übertragen
        new_img_2 = np.zeros(img.shape, dtype="uint8")
        r, c = new_img.shape
        for row in range(r):
            for column in range(c):
                if new_img[row][column] == True:
                    new_img_2[row][column] = 1

        # Binäres Bild zurückgeben
        return new_img_2

    @staticmethod
    def states(img, START_X_COORDINATE:int, STATE_DIMENSION:int, generated = False, ss_only = False):

        points = []
        states = []
        list = []

        height = None
        width = None


        if len(img.shape) == 3:
            line = Line.detect(img,generated)
        elif len(img.shape) == 2:
            line = img
        else:
            print('Error: falscher Übergabeparameter für img')
            exit()

        if START_X_COORDINATE < 0:
            print('Error: START_X_COORDINATE must be greater than 0')
            exit()
        
        height, width = line.shape

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

        if ss_only:
            point = points[0]
            y1 = point[1] - int(STATE_DIMENSION/2)
            y2 = point[1] + int(STATE_DIMENSION/2) +1
            x1 = point[0] - int(STATE_DIMENSION/2)
            x2 = point[0] + int(STATE_DIMENSION/2) +1
            states.append(line[y1:y2, x1:x2])

        else:
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

        
        return points, states

    @staticmethod
    def show(img, points, states, scale = 1, withpath = None):

        # Ergebnis anzeigen nur zur Visualisierung hat nichts mit der Bildverarbeitung zu tun
        
        print("INFO: press 'q' to close all windows and quit program")

        if scale <= 0:
            print('Error: scale value must be greater than 0')
            exit()

        if len(img.shape) == 3:
            height, width, dim = img.shape
        elif len(img.shape) == 2:
            height, width = img.shape
            img = cv2.cvtColor(img*255, cv2.COLOR_GRAY2BGR)
        else:
            print('Error: wrong parameter for img')
            exit()


        # Linie aus Punkten erstellen
        line = np.zeros((height, width), dtype="uint8")

        for point in points:
            line[point[1]][point[0]] = 255

        line_bgr = cv2.cvtColor(line, cv2.COLOR_GRAY2BGR)


        # Anzeigefenster erstellen
        window_size = (int(500*scale), int(500*scale))
        cv2.namedWindow('States', WINDOW_NORMAL)
        cv2.resizeWindow('States', window_size[0], window_size[1])

        window_size = (int(1200*scale), int(900*scale))
        cv2.namedWindow('Line', WINDOW_NORMAL)
        cv2.resizeWindow('Line', window_size[0], window_size[1])

        cv2.moveWindow('States', int(80), int(40*scale))
        cv2.moveWindow('Line', int(500*scale+100), int(40*scale))


        # Startbild anzeigen
        text = "press 's' to start or 'q' to quit"
        img = cv2.putText(img, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA, False)
        cv2.imshow('Line', img)

        while(1):
            k = cv2.waitKey(0) & 0xFF
            if k == ord('s'):
                break
            if k == ord('q'):
                cv2.destroyAllWindows()
                exit()

        path = []
        last_point = None
        
        # Video anzeigen
        for i in range(len(states)):

            if last_point is not None:

                delta_x = points[i][0] - last_point[0] 
                delta_y = points[i][1] - last_point[1] 

                path.append(Line.find_direction(delta_x, delta_y))

            line_bgr[points[i][1]][points[i][0]] = (0, 0, 255)
            cv2.imshow('Line', line_bgr)
            cv2.imshow('States', states[i]*255)
            k = cv2.waitKey(20) & 0xFF
            if k == ord('q'):
                cv2.destroyAllWindows()
                break
            
            last_point = [ points[i][0], points[i][1]  ]

        cv2.destroyAllWindows()

        if withpath:
            return ','.join(path)