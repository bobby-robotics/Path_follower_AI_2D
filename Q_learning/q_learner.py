import copy
import numpy as np
import pandas as pd
import os
from Q_learning.state import state
from Q_learning.enviroment import enviroment
from enum_motion import Motions
import cv2
from cv2 import WINDOW_NORMAL
import time
from math import sin,cos, pi

#*************************************
# State definition:
# [tcp_x_current, tcp_y_current, orientation_current]
# [tcp_x_target, tcp_y_target, orientation_targer]
#
#************************************
#
# Agent starting with epsilon value of 1 
# for taking a random action
# gradualy decriesing over time
# wtih value of 0.01 for each itteration.
#   
#
#************************************

class q_learner():
    
    header=["State\Action" ,"right","left","up","down","clockwise","counterclockwise"]

    img = None
    q_table = None
    file = None
    epsilon = 0
    #delta = 0.01
    state = None
    visualise = None

    def __init__(self, visualise) -> None:
        self.file = os.getcwd() + "/Q_learning/q_table.csv"
        self.import_q_table()

        self.visualise = visualise


    def init_params(self, img, initial_tcp, initial_img_matrix):

        self.img = img

        # starting point and orientation
        tool_def = np.zeros((5,5))
        tool_def[0,2] = 1
        tool_def[4,2] = 1
        tool_def[2,2] = initial_tcp[0] # tcp x
        tool_def[2,3] = initial_tcp[1]  # tcp y

        initial_state = np.array([initial_img_matrix, tool_def])

        self.state = state(initial_state)

    def import_q_table(self):

        if os.path.isfile(self.file):
            self.q_table = pd.read_table(self.file, delimiter=",|,\s+|\s+,")#,header=1)

        self.q_table = self.q_table.set_index(self.header[0]).T.to_dict('list')
        #print(self.q_table)

    def export_q_tabel(self):

        df = pd.DataFrame.from_dict(self.q_table,orient = 'index',dtype="float")

        df = df.reset_index()
        #print("\n", df)
        df.columns  = self.header
        df.set_index(self.header[0])

        print("\n", df)
        df.to_csv(self.file, index=False)

    def init_new_state(self):
        
        dict_key = hash(self.state)
        self.q_table[dict_key] = np.zeros(len(Motions))

    def state_existance(self):
        
        if hash(self.state) not in self.q_table:
            self.init_new_state()

        else:
            pass

    def choose_action(self):

        if np.random.random() < self.epsilon:

            # if random probability smaller than epsilon 
            # agent should choose a random action     
            return np.random.randint(0, len(Motions))
        
        else:
            # agent is now taking 
            # the best known action Q(s,a)
            return np.argmax(self.q_table.get(hash(self.state)))
    
    def greedy_exploration(self,offset):

        alpha = 0.2
        gamma = 0.8
        Ne = 500

        Nc = 1000

        env = None
        target_tcp = None

        targets = []

        wire  = np.where(self.img[:,:offset + 1] == 1)
        wire = np.asarray(wire).transpose()
        # print(wire)

        for w in wire:
            targets.append( hash(tuple(np.array([ w[1], w[0]]) )))

        np.random.seed(42)
        
        last_stable_state = None

        for nc in range(Nc):

            if nc == 0:
                env = enviroment(self.img, targets=targets,visualise=self.visualise)
            else:
                #self.state.set_state(last_stable_state)
                #print(self.state.get_tcp_xy())
                print("init env one more time")
                env = enviroment(self.img, target_tcp, targets, visualise=self.visualise, last_legit_state = self.state.get_state())


            for i in range(Ne):
                
                self.state_existance()
                a = self.choose_action()
                s = hash(self.state)
                row = self.q_table.get(s)

                self.state.set_state(env.update_state(a, self.state, self.visualise))

                s_prim = hash(self.state)
                self.state_existance()

                r, col = env.get_reward(self.state,a)

                row_prim = self.q_table.get(s_prim)

                row[a] = row[a] + alpha*( r + gamma*row_prim[np.argmax(self.q_table.get(hash(self.state)))] - row[a])

                self.q_table.update( {s : row} )
               

                if self.epsilon > 0.0:
                    self.epsilon -= 1/100

                print("Reward:" , r)
                # if collision detected, set back to 
                if col:
                    print("\nCollision:",col)
                    #target_tcp = env.get_last_target()
                    #targets = env.get_targets()
                    # time.sleep(3)
                    #last_stable_state = env.get_last_legit_state()
                    #self.state.set_state(env.get_last_legit_state())
                    break
                
                # if r == 10:
                #     print("Problem")
                #     self.state.set_state(env.get_last_legit_state())

                #last_stable_state = copy.deepcopy(self.state.get_state())
                # target_tcp = env.get_last_target()
                # targets = env.get_targets()

            # take last stable state
            self.state.set_state( env.get_last_legit_state() )
            target_tcp = env.get_last_target()
            targets = env.get_targets()
            
            self.epsilon = 1# - 1/Nc






        
   
    