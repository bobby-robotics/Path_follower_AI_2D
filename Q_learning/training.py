from DataGenerator.splines_generator import data_gen
from Bildverarbeitung.Final.Line import Line
from Bildverarbeitung.Final.take_pic import take_pic
from Q_learning.q_learner import q_learner
import numpy as np
import cv2
from cv2 import WINDOW_NORMAL
import os
import time

class training():

    imgs = None
    ps = []
    mats = []
    offset = None
    visualise = None
    execution = None
    end_x = None

    # agent (q learner)
    q = None

    # offset = offset from the left to the right for so that we can have a line from 0 to offset
    # amount of imgs = number of images to be created (self explanatory)
    # visualise = if set True we will see the progress of learning and execution
    # execution = if set True, there will be no generated data, but an image should be taken
    # after calling the "execute" method in this class
    def __init__(self, offset = 20, amount_of_imgs = 0, end_x = 540,  visualise = False, execution = False) -> None:

        self.execution = execution
        self.end_x = int(end_x)

        if execution == False:
            # Generate Data
            data = data_gen( amount_of_imgs, 4, 640, 480,offset + 2)
            data.splines_generator()
            #data.save_gen_imgs()
            self.imgs = data.get_gen_imgs()

        self.offset = offset

        self.visualise = visualise

        # init q learner
        self.q = q_learner(self.visualise) 

     # finding the start and end point for the agent
    # and taking the first 5x5 matrix from the starting point
    def take_init_param(self,img):

        point = np.where(img[:,self.offset] == 1)
        point = np.asarray(point).transpose()

        y1 = point[0][0] - 3
        y2 = point[0][0] + 4
        x1 = self.offset - 3 
        x2 = self.offset + 4 

        matrix = img[y1:y2, x1:x2]

        # last target
        point2 = np.where(img[:,self.end_x] == 1)
        point2 = np.asarray(point2).transpose()

        return point,point2,matrix

    # self explanatory
    def train(self):

        for img in self.imgs:

            cv2.imshow("Image To Train:",img*255)
            cv2.waitKey(1500)
            self.train_for_img(img)

            #s = self.train_for_img(img, self.q, True, ',')
            #print(s)
            #time.sleep(5)

            # img_now = np.zeros((264,264),dtype=int)

        self.q.export_q_tabel()

    # img = image
    # q = Q-learner (Agent)
    # execution = if set to True will give the oprimal policy back
    # delimiter = free to chose delimiter, must be one char long        
    def train_for_img(self, img, take_policy = False, delimiter = ''):

        point, point2, matrix = self.take_init_param(img)

        #print(np.array([self.offset, point[0][0]]), matrix, np.array( [self.end_x, point2[0][0]] ))

        self.q.init_params(img, np.array([self.offset, point[0][0]]), matrix, np.array( [self.end_x, point2[0][0]] ))

        success = False
        if take_policy == False:
            self.q.run_greedy_exploration(self.offset)

        else: 
            while success == False:
                movements, success = self.q.optimal_policy(self.offset, delimiter = delimiter)
                if success:
                    break
                self.q.init_params(img, (self.offset, point[0][0]), matrix, np.array( [self.end_x, point2[0][0]] ))
                self.q.run_greedy_exploration(self.offset)
                self.q.init_params(img, (self.offset, point[0][0]), matrix, np.array( [self.end_x, point2[0][0]] ))

            #movements, success = self.q.optimal_policy(self.offset, delimiter = delimiter)
            return  movements

    # taking a pic and doing some operations with Line.detect(img)
    # so that we can have a binary pic
    # which our agent can learn and make an optimal policy for
    def execute(self, img, delimiter = '', camid = 1):

        cv2.imshow("Line",img)
        cv2.waitKey(2000)

        c = 'n'
        filter_size = 1

        while(c == 'n'):

            img2 = Line.detect(img, filter_size)
            cv2.imshow("Thinned Line:",img2*255)
            cv2.waitKey(2000)
            c = str(input("Good?y/n"))
            if c == 'y':
                break
            filter_size +=2
            #img = take_pic.get_pic(camid)

        s = self.train_for_img(img2, take_policy = True, delimiter = delimiter)

        self.q.export_q_tabel()

        return s

