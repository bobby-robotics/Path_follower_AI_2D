
from DataGenerator.fake_path_from_image import fake_path_from_image
from Bildverarbeitung.Calibration.four_points_method import four_points_method
from Bildverarbeitung.Final.take_pic import take_pic
import os
import cv2
import numpy as np
from math import sin,cos, pi,sqrt
from enum_motion import Motions
from cv2 import WINDOW_NORMAL
from Q_learning.training import training

def test_rotation():
    alpha = -(-45)*pi/180
    rot = np.zeros((2,2))
    rot[0,0] = cos(alpha)
    rot[0,1] = -sin(alpha)
    rot[1,0] = sin(alpha)
    rot[1,1] = cos(alpha)

    print(rot)

    vector = np.array([2,0])
    # vector[0] -= 2
    # vector[1] -= 2
    
    vector1 = np.array([2,4])
    # vector1[0] -= 2
    # vector1[1] -= 2

    vector[0] -= 2
    vector[1] -= 2
    vector1[0] -= 2
    vector1[1] -= 2

    # matr = np.zeros((5,5))
    # matr[vector[1] +  2,vector[0]+2] = 1
    # matr[vector1[1] + 2,vector1[0]+2] = 1
    # matr[2,2] = 255

    
    # indexes  = np.where(matr == 1)
    # indexes = np.asarray(indexes).transpose()
    # print(indexes)
    # print(len(indexes))
    # print(indexes[0][1], indexes[0][0])
    # print(indexes[1][1], indexes[1][0])
    # for i in range(matr.shape[0]):
    #     indexes  = np.where(matr[i:] == 1)
    #     if indexes is not None:
    #         print(i,indexes[0])

    img = np.zeros((5,5))
    for i in range(20):
        
        img[vector[1] +  2,vector[0]+2] = 255
        img[vector1[1] + 2,vector1[0]+2] = 64
        cv2.namedWindow('State', WINDOW_NORMAL)
        cv2.resizeWindow('State', 500,500)
        cv2.imshow("State",img)
        cv2.waitKey(500)

        # transform

        if 1 in np.absolute(vector):
            vector = vector*sqrt(2)

        if 1 in np.absolute(vector1):
            vector1 = vector1*sqrt(2)

        vector = np.matmul(rot,vector)
        vector1 = np.matmul(rot,vector1)

        vector = (vector).astype("int")

        vector1 = (vector1).astype("int")        

        print("vector:",vector+2)
        print("vector1:",vector1+2)

        np.where(img == 1,img, img-1)

def test_pix_mm():
    fpm = four_points_method()
    tf = fpm.get_transform_from_pix_mm() 
    print("tf\n", tf)

    #frame = take_pic.get_pic(1) # get the taken pic/frame from the choosen webcam

    p_pix =  np.array( [106, 258, 1] )
    p_mm = np.array([158.38, 677.15, -23.29, 1])

    xyz_v = tf.dot(p_pix)
    print("pix-> xyz:", xyz_v,sep="\n")

    print(hash(tuple(tf.flat)))

    tf = np.linalg.pinv(tf)
    print("tf",tf)
    uv_v = np.matmul(tf,p_mm.transpose())
    print("xyz->pix:", uv_v, sep="\n")

    print(fpm.get_transform_from_pix_mm())


def main():

    t = training(10,20, True)

    t.start_training()    

    

if __name__ == '__main__':
    main()