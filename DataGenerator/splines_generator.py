import scipy
import numpy as np
from scipy import interpolate
import matplotlib
from matplotlib import pyplot as plt

#Class Data Generator 
#Task: Generates trainings images 
#for the agent
class Data_Gen:

    #Number of data (images) to be created
    num_of_data_imgs = 0

    #Number of points per spline
    num_of_points = 0;

    #X-Axis lenght
    x_axis_lenght = 0

    #X-Axis separations
    x_axis_sep  = 0

    #
    images_data = None

    #Init defines the number of images, points per spline
    #and the lenght of the X-Axis
    def __init__(self, num_of_data_imgs, num_of_points, x_axis_lenght) -> None:
        
        self.num_of_data_imgs = num_of_data_imgs
        self.num_of_points = num_of_points
        self.x_axis_lenght = x_axis_lenght

        self.x_axis_sep = np.linspace( 0, self.x_axis_lenght, num = self.num_of_points )
        #self.images_data = np.ndarray(self.num_of_data_imgs)
        self.images_data = []

        self.splines_generator()

    #Splines Generator
    #Task: Generates Splines from points
    def splines_generator(self):
        
        for i in range(self.num_of_data_imgs):
            random_point = np.random.randint( low = 200, high = 500, size = self.num_of_points, dtype = int)

            self.images_data.append( interpolate.interp1d( x = self.x_axis_sep, y = random_point, kind = 'zero') )
            
            ynew = self.images_data[i]( self.x_axis_sep )

            print("TEST")
            plt.plot(self.x_axis_sep, ynew)
            plt.ylim(0, 600)
            plt.show()

           