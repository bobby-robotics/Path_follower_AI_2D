from DataGenerator.splines_generator import data_gen
from Bildverarbeitung.Final.Line import Line
from Q_learning.q_learner import q_learner
import numpy as np
import cv2

class training():

    imgs = None
    ps = []
    mats = []
    offset = None
    visualise = None

    def __init__(self,amount_of_imgs, offset, visualise = False) -> None:
        # Generate Data
        data = data_gen( amount_of_imgs, 4, 640, 480,offset + 2)
        data.splines_generator()
        data.save_gen_imgs()
        self.imgs = data.get_gen_imgs()

        self.offset = offset

        self.visualise = visualise

    def start_training(self):
        
        # init q learner
        q = q_learner(self.visualise) 

        for img in self.imgs:

            point = np.where(img[:,self.offset] == 1)
            point = np.asarray(point).transpose()
            #print(point)

            y1 = point[0][0] - 2
            y2 = point[0][0] + 3
            x1 = self.offset - 2 
            x2 = self.offset + 3 

            matrix = img[y1:y2, x1:x2]

            #print(matrix)

            # ps, mats = Line.states(img, 20, 5,ss_only=True)
            #print(self.offset, point[0][0])
            q.init_params(img, (self.offset, point[0][0]), matrix)

            q.greedy_exploration()


        q.export_q_tabel()
            