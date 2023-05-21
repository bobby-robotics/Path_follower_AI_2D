import copy
import numpy as np
import pandas as pd
import os
from Q_learning.state import state
from Q_learning.eviroment import enviroment
from enum_motion import Moutions
import cv2
from cv2 import WINDOW_NORMAL

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
    
    header=["State\Action" ,"up","down","left","right","clockwise","counterclockwise"]

    img = None
    q_table = None
    file = None
    epsilon = 1
    delta = 0.01
    state = None

    def __init__(self) -> None:

        self.file = os.getcwd() + "/Q_learning/q_table.csv"

        self.import_q_table()
        np.random.seed(9001)



        #print(self.state.get_state()[0],"\n", self.state.get_state()[1])

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
        print("\n", df)
        df.columns  = self.header
        df.set_index(self.header[0])

        print("\n", df)
        df.to_csv(self.file, index=False)

    def init_new_state(self):
        
        dict_key = hash(self.state)
        self.q_table[dict_key] = np.zeros(len(Moutions))

    def state_existance(self):
        
        if hash(self.state) not in self.q_table:
            self.init_new_state()

        else:
            pass

    def choose_action(self):

        if np.random.random() < self.epsilon:

            # if random probability smaller than epsilon 
            # agent should choose a random action     
            return np.random.randint(0, len(Moutions) - 1)
        
        else:
            # agent is now taking 
            # the best known action Q(s,a)
            return np.argmax(self.q_table.get(hash(self.state)))
            # hashed_state = self.__hash__()

            # if hashed_state in self.q_table:
            #     # agent is now taking 
            #     # the best known action Q(s,a)
            #     return np.argmax(self.q_table.get(hashed_state))
            
            # else:

            #     return np.random.randint(low = 0, high = len(Moutions), size = 1, dtype = "int16" )[0] #self.choose_action()
    
    def greedy_exploration(self):

        alpha = 0.5
        gamma = 0.5
        Ne = 100

        Nc = 1000

        # d = {1 :["one","one","one"], 2: "two"}   
        # ne = d.get(1)
        # ne[1] = "Three"
        # ml = {1 : ne}
        # d.update(ml)
        # print(d.get(1))

        env = None

        cv2.namedWindow('tcp', WINDOW_NORMAL)
        cv2.resizeWindow('tcp', 500,500)

        cv2.namedWindow('wire', WINDOW_NORMAL)
        cv2.resizeWindow('wire', 500,500)

        # cv2.imshow("img_2",img_2)
        # cv2.waitKey(0)
        
        last_stable_state = None

        for nc in range(Nc):

            if nc == 0:
                env = enviroment(self.img, self.state.get_tcp_xy(),self.state)
            else:
                self.state.set_state(last_stable_state.get_state())
                env = enviroment(self.img, self.state.get_tcp_xy(),self.state)

            for i in range(Ne):
            
                self.state_existance()

                a = self.choose_action()

                tcp = np.array(self.state.get_tcp_xy()).astype(int)

                cv2.imshow("wire", self.state.get_state()[0])
                cv2.imshow("tcp", self.state.get_state()[1])
                cv2.waitKey(50)

                s = hash(self.state)
                # print(s)

                self.state.set_state(env.update_state(a))

                s_prim = hash(self.state)

                self.state_existance()

                r = env.get_reward()
                print("Reward:" , r)

                if abs(r) > 50:
                    break

                row = self.q_table.get(s)

                row_prim = self.q_table.get(s_prim)

                row[a] = row[a] + alpha*( r + gamma*row_prim[np.argmax(self.q_table.get(hash(self.state)))] + row[a])

                self.q_table.update( {s : row} )

                if self.epsilon > 0.0:
                    self.epsilon -= 1/Ne

                wire = np.where(self.state.get_state()[0])
                wire = np.asarray(wire).transpose()
                #print(wire)
                if len(wire) < 5:
                    print("No Wire There!")
                    break

                last_stable_state = copy.deepcopy(self.state)






        
   
    