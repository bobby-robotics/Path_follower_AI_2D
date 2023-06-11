import copy
import numpy as np
import pandas as pd
import os
from Q_learning.state import state
from Q_learning.enviroment import enviroment
from Q_learning.enum_rewards import rewards
from enum_motion import Motions
import cv2
from cv2 import WINDOW_NORMAL
import time
from math import sin,cos, pi 
import datetime

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
    state = None
    visualise = None
    last_target = None
    initial_tcp = None
    initial_img_matrix = None
    # epoch time
    epoch_time = datetime.datetime(2000, 1, 1)
    

    def __init__(self, visualise) -> None:
        self.file = os.getcwd() + "/Q_learning/q_table.csv"
        self.import_q_table()

        self.visualise = visualise

    def init_params(self, img, initial_tcp, initial_img_matrix, last_target):

        self.img = img
        self.initial_tcp = initial_tcp
        self.initial_img_matrix = np.array(initial_img_matrix)

        # starting point and orientation
        tool_def = np.zeros((7,7))
        tool_def[0,3] = 1
        tool_def[6,3] = 1
        tool_def[3,3] = initial_tcp[0] # tcp x
        tool_def[3,4] = initial_tcp[1]  # tcp y
        tool_def[0,6] = 90

        initial_state = np.array([initial_img_matrix, tool_def])

        self.state = state(initial_state)

        self.last_target = last_target
        
    def import_q_table(self):

        if os.path.isfile(self.file):
            self.q_table = pd.read_table(self.file, delimiter=",|,\s+|\s+,")

        self.q_table = self.q_table.set_index(self.header[0]).T.to_dict('list')

    def export_q_tabel(self):

        df = pd.DataFrame.from_dict(self.q_table,orient = 'index',dtype="float")

        df = df.reset_index()
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
            a = np.random.randint(0, len(Motions))
            dt = datetime.datetime.now()   
            delta = int((dt - self.epoch_time).total_seconds())
            np.random.seed(a*delta)   
            return a
        
        else:
            # agent is now taking 
            # the best known action Q(s,a)
            print("not random")
            return np.argmax(self.q_table.get(hash(self.state)))
    
    def get_first_targets(self,offset):

        targets = []

        # look for wire anywhere on y 
        # and from 0 x to offset + 1 x
        wire  = np.where(self.img[:,:offset + 1] == 1)
        wire = np.asarray(wire).transpose()

        # hashing the x,y coordinates
        # and saving them as "known" targets
        for w in wire:
            targets.append( hash(tuple(np.array([ w[1], w[0]]) )))

        return targets        

    def existance_update(self, env, optimal_policy = False):

        self.state_existance()
        a = self.choose_action()
        s = hash(self.state)
        row = self.q_table.get(s)

        self.state.set_state(env.update_state(a, self.state, self.visualise, optimal_policy))

        return a, s, row

    def run_greedy_exploration(self, offset):

        while(self.greedy_exploration(offset) == False):
                self.init_params(self.img, self.initial_tcp, self.initial_img_matrix, self.last_target)
                #time.sleep(1)

    def greedy_exploration(self,offset):
        
        i = 0
        Nc = 250
        env = None
        end = False
        dist = 0
        alpha = 0.8
        gamma = 0.5
        first_try = False
        target_tcp = None
        targets = self.get_first_targets(offset)
        
        self.epsilon = 0

        for nc in range(1,Nc+1):

            if i == 0:
                i += 1
                env = enviroment(self.img, targets=targets,visualise=self.visualise)
            else:
                i += 1
                print("init env one more time")
                env = enviroment(self.img, target_tcp, targets, visualise=self.visualise, last_legit_state = self.state.get_state(),dist = dist)
                
            col = False
            while(col == False):

                a, s, row = self.existance_update(env)

                s_prim = hash(self.state)
                self.state_existance()

                r, col, itr = env.get_reward(self.state,a)

                row_prim = self.q_table.get(s_prim)

                row[a] = row[a] + alpha*( r + gamma*row_prim[np.argmax(self.q_table.get(hash(self.state)))] - row[a])

                self.q_table.update( {s : row} )

                if itr:
                    break

                print("Reward:" , r)
                # if len(np.where(self.state.get_state()[0] == 1)) > 5:
                #     end = True
                #     print(i)
                #     break
                    
                if self.state.get_tcp_xy()[0] == self.last_target[0] and self.state.get_tcp_xy()[1] == self.last_target[1]:
                    end = True
                    print(i)
                    #time.sleep(15)
                    break

                if self.epsilon > 0.0:
                    self.epsilon -= 1/20  

            # take last stable state
            self.state.set_state( env.get_last_legit_state() )
            target_tcp = env.get_last_target()
            targets = env.get_targets()
            dist = env.get_dist()

            if i == 1 and col == False and end:
                first_try = True
                break
            else:
                first_try = False
            if end:
                break
            
            self.epsilon =1 - nc/Nc

        return first_try
   
    def optimal_policy(self, offset ,delimiter = ''):

        end = True
        success = True
        movements = []
        targets = self.get_first_targets(offset)
        env = enviroment(self.img, targets=targets,visualise=True)

        while(end):
            a, s, row = self.existance_update(env, True)

            movements.append(Motions(a).name)

            r, col, itr = env.get_reward(self.state,a)

            if col or itr:
                movements = []
                success = False
                break

            if len(np.where(self.state.get_state()[0] == 1)) > 5:
                end = False
                break
                
            elif self.state.get_tcp_xy()[0] == self.last_target[0] and self.state.get_tcp_xy()[1] == self.last_target[1]:
                end = False
                break
        
        print(len(movements))
        return delimiter.join(movements), success

            
            