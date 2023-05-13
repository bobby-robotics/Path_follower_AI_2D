from DataGenerator.splines_generator import data_gen
from DataGenerator.fake_path_from_image import fake_path_from_image
from Bildverarbeitung.Calibration.four_points_method import four_points_method
from Bildverarbeitung.Final.take_pic import take_pic
import os
import cv2

def main():

    #data = data_gen( 10, 5, 1280, 720)
    #data.splines_generator()

    img = cv2.imread(os.path.abspath('Bildverarbeitung/IMG/line1.jpg'))
    if img is None:
        print('Error: file could not be found or read.')
        exit()

    fpm = four_points_method()

    frame = take_pic.get_pic()

    

    print(fpm.get_transform_from_pix_mm())

    #print(fake_path_from_image.create_fake_path(img, 20, 5))
    

if __name__ == '__main__':
    main()