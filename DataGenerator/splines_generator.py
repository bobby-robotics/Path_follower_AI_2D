import cv2
import random
import os
import numpy as np
from datetime import datetime
from scipy.interpolate import CubicSpline
from skimage.morphology import skeletonize
from DataGenerator.correct_splines import correct_spline

#Class Data Generator 
#Task: Generates trainings images 
#for the agent
class data_gen:

    #Number of data (images) to be created
    num_of_data_imgs = 0

    #Number of points per spline
    num_of_points = 0

    #X-Axis lenght (image width)
    width = 0

    #Y-Axis height (image height)
    height = 0

    #image canvas
    canvas = None

    #X-Axis separations
    x_axis_sep  = []

    #list for interpolated points 
    interpolation = None

    #current working directory
    cwd = None

    # generated imgs
    gen_imgs = []

    # offset from the side
    offset = None
    
    end_point_x = 530


    #Init defines the number of images, points per spline
    #and the lenght of the X-Axis
    def __init__(self, num_of_data_imgs, num_of_points, width, height, offset) -> None:
        
        self.num_of_data_imgs = num_of_data_imgs
        self.num_of_points = num_of_points
        self.width = width
        self.height = height
        self.offset = offset

        
        self.x_axis_sep = np.linspace( offset, self.end_point_x, num = self.num_of_points )

        cwd_ = os.getcwd

        self.cwd = cwd_() + "\\generated_images"
        print(self.cwd)

    #Splines Generator
    #Task: Generates Splines from points
    def splines_generator(self):


        #create a canvas width x height
        self.canvas = np.zeros((self.height, self.width), dtype="uint8")

        x_axis_arr = np.arange(self.offset, self.end_point_x, 1, dtype = "int")

        #low and high range for the random nuber generator
        low = self.height/2 - self.height/4
        high = self.height/2 + self.height/4


        for i in range(self.num_of_data_imgs):

            #list of random numbers
            random_point = np.random.randint( low = low, high = high, size = self.num_of_points, dtype = int)

            # height of the original loop starting/ending point
            random_point[-1] = 289
            random_point[0] = 289

            self.interpolation = CubicSpline(self.x_axis_sep, random_point)

            k = zip(x_axis_arr, self.interpolation(x_axis_arr))

            for x, y in k:
                self.canvas[ int(y), x] = 255

            y = random_point[0]
            for i in range(0,self.offset):
                self.canvas[y,i] = 255
                self.canvas[y, i + self.end_point_x ] = 255

            cv2.imshow("non-continuous", self.canvas)
            cv2.waitKey(0)

            img = correct_spline.thinning(self.canvas)
            
            cv2.imshow("continuous", img*255)
            cv2.waitKey(0)

            self.gen_imgs.append(img)

            #create a canvas width x height
            self.canvas = np.zeros((self.height, self.width), dtype="uint8")

    def save_gen_imgs(self):

        for img in self.gen_imgs:
            curr_time =  "\\" + datetime.now().strftime('%Y-%m-%d_%H_%M_%S') 
            cv2.imwrite(self.cwd + curr_time + ".jpeg", img*255 )

    def get_gen_imgs(self):
        return self.gen_imgs
