
from DataGenerator.fake_path_from_image import fake_path_from_image
from Bildverarbeitung.Calibration.four_points_method import four_points_method
from Bildverarbeitung.Final.take_pic import take_pic
import os
import cv2
import numpy as np
from math import sin,cos, pi,sqrt

from XMLParser.StringCompressionAndSplitting import StringCompressionAndSplitting
from XMLParser.XMLParser import XMLParser
from enum_motion import Motions
from cv2 import WINDOW_NORMAL
from Q_learning.training import training
import time 

def test_rotation():
    alpha = -(-45)*pi/180
    rot = np.zeros((2,2))
    rot[0,0] = cos(alpha)
    rot[0,1] = -sin(alpha)
    rot[1,0] = sin(alpha)
    rot[1,1] = cos(alpha)

    print(rot)

    vector = np.array([3,0])
    # vector[0] -= 2
    # vector[1] -= 2
    
    vector1 = np.array([3,6])
    # vector1[0] -= 2
    # vector1[1] -= 2

    vector[0] -= 3
    vector[1] -= 3
    vector1[0] -= 3
    vector1[1] -= 3

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

    img = np.zeros((7,7))
    for i in range(20):
        
        img[vector[1] +  3,vector[0]+3] = 1
        img[vector1[1] + 3,vector1[0]+3] = 1
        cv2.namedWindow('State', WINDOW_NORMAL)
        cv2.resizeWindow('State', 500,500)
        cv2.imshow("State",img)
        cv2.waitKey(500)

        # transform

        if 2 in np.absolute(vector):
            vector = vector*(sqrt(2)/4)

        if 2 in np.absolute(vector1):
            vector1 = vector1*(sqrt(2)/4)

        

        vector = np.matmul(rot,vector)
        vector1 = np.matmul(rot,vector1)

        print(vector+3)
        print(vector1+3)

        vector = (vector).astype("int")

        vector1 = (vector1).astype("int")        

        print("vector:",vector+3)
        print("vector1:",vector1+3)

        np.where(img == 1,img, img-1)

        time.sleep(5)

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

def test_randomness():
    print(len(Motions) - 1)
    i = 0
    np.random.seed(13)#[42,1,3,56,2,7,1,23,5,16,8,3,3,21,3])
    while (np.random.randint(0, len(Motions) ) != 5 ):
        print(i)
        i+=1
        #time.sleep(1)
        #np.random.seed(np.random.randint(0, len(Motions) ))
    time.sleep(1)
    while (np.random.randint(0, len(Motions) ) != 5 ):
        print(i)
        i+=1

def main():

    #teststring = "rrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrr"

    t = training(offset = 20,amount_of_imgs=1, visualise = True)

    t.train()    
    # np.random.seed(42)
    # for i in range(200):
    #     a = np.random.random()
    #     print(a)
    #     print(int(a*10))
    #     np.random.seed(int(a*10))
    #img = take_pic.get_pic(1)

    trainee = training(offset = 20, end_x= 530 ,visualise=True,execution=True)

    cwd = os.getcwd()

    for file in os.listdir(cwd+"/taken_images"):
        #rint(file)
        if file.endswith(".jpeg"):
            img = cv2.imread(os.path.abspath('taken_images/'+file))
            if img is None:
                print('Error: file could not be found or read.')
                exit()
            print(trainee.execute(img))



if __name__ == '__main__':
    main()