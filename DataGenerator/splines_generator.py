import scipy
import numpy as np
from scipy import interpolate
import matplotlib
from matplotlib import pyplot as plt
import cv2
import random
from scipy.interpolate import CubicSpline
import os
from datetime import datetime

#Class Data Generator 
#Task: Generates trainings images 
#for the agent
class data_gen:

    #Number of data (images) to be created
    num_of_data_imgs = 0

    #Number of points per spline
    num_of_points = 0;

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


    #Init defines the number of images, points per spline
    #and the lenght of the X-Axis
    def __init__(self, num_of_data_imgs, num_of_points, width, height) -> None:
        
        self.num_of_data_imgs = num_of_data_imgs
        self.num_of_points = num_of_points
        self.width = width
        self.height = height

        self.x_axis_sep = np.linspace( 0, self.width, num = self.num_of_points )

        cwd_ = os.getcwd

        self.cwd = cwd_() + "\\generated_images"
        print(self.cwd)

    #Splines Generator
    #Task: Generates Splines from points
    def splines_generator(self):

        #create a canvas width x height
        self.canvas = np.zeros((self.height, self.width), dtype="uint8")

        x_axis_arr = np.arange(0, self.width, 1, dtype = "int")

        #low and high range for the random nuber generator
        low = self.height/2 - self.height/4
        high = self.height/2 + self.height/4


        for i in range(self.num_of_data_imgs):

            #list of random numbers
            random_point = np.random.randint( low = low, high = high, size = self.num_of_points, dtype = int)

            self.interpolation = CubicSpline(self.x_axis_sep, random_point)

            k = zip(x_axis_arr, self.interpolation(x_axis_arr))

            for x, y in k:
                self.canvas[ int(y), x] = 255

            cv2.imshow("Canvas", self.canvas)
            cv2.waitKey(0)
            
            curr_time =  "\\" + datetime.now().strftime('%Y-%m-%d_%H_%M_%S') 
            cv2.imwrite(self.cwd + curr_time + ".jpeg", self.canvas )
            #create a canvas width x height
            self.canvas = np.zeros((self.height, self.width), dtype="uint8")

class simple_spline:

    canvas = None 
    width = 0
    height = 0

    def __init__(self, width, height) -> None:

        self.width = width
        self.height = height

        self.canvas = np.zeros((height, width, 3), dtype="uint8")


    def draw_spline(self):
        
        #cv2.imshow("Canvas", self.canvas)
        #cv2.waitKey(0)

        offset = 2

        
        for i in range(0,5):

            pix_0 = np.random.randint(self.height/2 - self.height/4, self.height/2 + self.height/4, size = 1)[0]

            print(pix_0)
            self.canvas[pix_0, 0] = 255

            for i in range(1, self.width):
                
                #pix_0 = np.random.randint(pix_0 - offset, pix_0 + offset, size = 1)[0]
                pix_0 = int(random.uniform(pix_0 - offset, pix_0 + offset))
                print(pix_0)
                if pix_0 <= 0.1*self.height:
                    pix_0 = pix_0 + offset
                    cv2.circle(self.canvas, (i, pix_0), 5, (128, 0, 255), 3)
                    cv2.circle(self.canvas, (i, pix_0), 1, (128, 0, 255), 3)
                else:
                    self.canvas[pix_0, i] = 255

                

                
            cv2.imshow("Canvas", self.canvas)
            cv2.waitKey(0)

            self.canvas = np.zeros((self.height, self.width, 3), dtype="uint8")

    def quadratic_spline(self):
        
            A = random.uniform(-5,5)
            B = random.uniform(-5,5)
            C = random.uniform(-5,5)

            pix_0 = int(A*pow(0, 2) + B*pow(0, 1) + C)

            self.canvas[pix_0, 0] = 255

            for i in range(1, self.height):

                pix_0 = int(A*pow(i, 2) + B*pow(i, 1) + C)
                print(pix_0)
                self.canvas[pix_0, i] = 255

                
            cv2.imshow("Canvas", self.canvas)
            cv2.waitKey(0)

            self.canvas = np.zeros((self.height, self.width, 3), dtype="uint8")