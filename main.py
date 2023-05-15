from DataGenerator.splines_generator import data_gen
from DataGenerator.fake_path_from_image import fake_path_from_image
from Bildverarbeitung.Calibration.four_points_method import four_points_method
from Bildverarbeitung.Final.take_pic import take_pic
import os
import cv2
import numpy as np

def main():

    # Generate Data
    #data = data_gen( 10, 5, 1280, 720)
    #data.splines_generator()

    # img = cv2.imread(os.path.abspath('Bildverarbeitung/IMG/line1.jpg'))
    # if img is None:
    #     print('Error: file could not be found or read.')
    #     exit()

    fpm = four_points_method()
    tf = fpm.get_transform_from_pix_mm()

    frame = take_pic.get_pic(1) # get the taken pic/frame from the choosen webcam

    p_pix =  np.array( [106, 258, 1] )
    p_mm = np.array([158.38, 677.15, -23.29, 1])

    xyz_v = tf.dot(p_pix)
    print("pix-> xyz:", xyz_v,sep="\n")


    tf = np.linalg.pinv(tf)
    uv_v = tf.dot(p_mm)
    print("xyz->pix:", uv_v, sep="\n")

    print(fpm.get_transform_from_pix_mm())

    
    # making a fake path only for testing
    #print(fake_path_from_image.create_fake_path(img, 20, 5))
    

if __name__ == '__main__':
    main()