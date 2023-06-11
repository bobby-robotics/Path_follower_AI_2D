from enum_motion import Motions
import numpy as np
from Q_learning.enum_rewards import rewards
# from Q_learning.state import state
from math import sin,cos, pi, sqrt
import cv2
from cv2 import WINDOW_NORMAL
import copy
import time
from math import sin,cos,asin,acos, pi, tan,atan, atan2
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

class enviroment():

    max_iterrations = 6

    img = None
    img_2 = None
    last_legit_state = None
    target_tcp = None
    tcp_on_target = False
    targets = None
    counter = None
    dist = None
    visualise = False

    def __init__(self, img, target_tcp = None, targets = None, visualise = False, last_legit_state = None, dist = 0) -> None:
        
        self.counter = 0
        self.dist = dist

        self.visualise = visualise
        self.img = img

        self.target_tcp = target_tcp

        self.targets = targets

        self.last_legit_state = copy.deepcopy(last_legit_state)

        if visualise:
            self.img_2 = cv2.cvtColor(self.img*255, cv2.COLOR_GRAY2BGR)

            cv2.namedWindow('s_tcp', WINDOW_NORMAL)
            cv2.resizeWindow('s_tcp', 400,400)

            cv2.namedWindow('s_wire', WINDOW_NORMAL)
            cv2.resizeWindow('s_wire', 400,400)

            cv2.namedWindow('enviroment', WINDOW_NORMAL)
            cv2.resizeWindow('enviroment', 1280,720)
        
    def rotate_translate(self, temp_state, theta):

        # Rotation to be done
        # Rotation Matrix 2D
        # with minus because coordinate System is
        # x for width, y height and z in the sreen 
        # so that if I want to rotate clockwise 
        # I need to rotate with a negative angle from my perspective
        # and a positive one for the screen 
        alpha = -theta*pi/180
        rot = np.zeros((2,2))
        rot[0,0] = cos(alpha)
        rot[0,1] = -sin(alpha)
        rot[1,0] = sin(alpha)
        rot[1,1] = cos(alpha)

        # look for electodes
        indexes  = np.where(temp_state[1] == 1)
        indexes = np.asarray(indexes).transpose()

        pos1 = None
        pos2 = None

        # if only 2 found it's all good
        sh = int((temp_state[1].shape)[0]/2)
        if len(indexes) == 2:
            pos1 = np.array([indexes[0][1], indexes[0][0]])
            temp_state[1][pos1[1],pos1[0]] = 0
            pos1[0] -= sh
            pos1[1] -= sh
        
            pos2 = np.array([indexes[1][1], indexes[1][0]])
            temp_state[1][pos2[1],pos2[0]] = 0
            pos2[0] -= sh
            pos2[1] -= sh
            
            

        else:
            print(temp_state[1])
            raise Exception("Found more than 2 Electrodes! Not Possible")
        
        #Transform 
        if 2 in np.absolute(pos1):
            pos1 = pos1*(3*sqrt(2)/4)

        if 2 in np.absolute(pos2):
            pos2 = pos2*(3*sqrt(2)/4)

        pos1 = np.matmul(rot,pos1)
        pos2 = np.matmul(rot,pos2)

        pos1 = (pos1).astype("int") 
        pos1[0] += sh
        pos1[1] += sh

        pos2 = (pos2).astype("int")
        pos2[0] += sh
        pos2[1] += sh

        temp_state[1][pos1[1],pos1[0]] = 1
        temp_state[1][pos2[1],pos2[0]] = 1

        return temp_state

    def get_last_target(self):
        return self.target_tcp

    def get_targets(self):
        return self.targets

    def get_dist(self):
        return self.dist

    def update_state(self, action_nr, state, visualise , optimal_policy):
        
        self.counter += 1
        if self.target_tcp is None or self.tcp_on_target:
            self.tcp_on_target = False
            self.find_target(state)
            self.last_legit_state = copy.deepcopy(state.get_state())
            self.dist = self.distance_to_target(state)

        if visualise:
            cv2.imshow("s_wire", state.get_state()[0])
            cv2.imshow("s_tcp", state.get_state()[1])

        action_vector = self.action_nr_to_vector(action_nr)

        temp_state = state.get_state()

        tcp = state.get_tcp_xy()

        tcp[0] += action_vector[0]
        tcp[1] += action_vector[1]

        sh = (temp_state[0].shape)[0]

        # cut a 7x7 matrix from the image
        y1 = int(tcp[1] - int(sh/2)    )     
        y2 = int(tcp[1] + int(sh/2) + 1)   
        x1 = int(tcp[0] - int(sh/2)    )     
        x2 = int(tcp[0] + int(sh/2) + 1)  
           
        # take new 7x7 matrix from the wire
        temp_state[0] = self.img[y1:y2, x1:x2]

        # update x,y and orientation
        temp_state[1][int(sh/2),int(sh/2)] += int(action_vector[0])
        temp_state[1][int(sh/2),int(sh/2)+1] += int(action_vector[1]) 
        temp_state[1][0,int(sh)-1] += int(action_vector[2])

        temp_state = self.rotate_translate(temp_state, action_vector[2])

        if optimal_policy:
                cv2.putText(img=self.img_2, text='Execution: taking optimal policy', org=(20, 40), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=1)
                visualise = True

        if visualise:
            self.img_2[int(tcp[1]),int(tcp[0])] = (0, 0, 255)
            cv2.imshow("s_wire", state.get_state()[0])
            cv2.imshow("s_tcp", state.get_state()[1])
            cv2.imshow("enviroment",self.img_2)
            
            cv2.waitKey(20)

       # print(temp_state)

        return copy.copy(temp_state)

    def find_target(self,state):
        
        wire = state.get_state()[0]
        sh = int(wire.shape[0]/2)

        wire  = np.where(wire[sh -1 :sh+2,sh-1:sh+2] == 1)
        wire = np.asarray(wire).transpose()

        tcp = state.get_tcp_xy()

        for i in range(len(wire)):
            wire[i,0] -= 1
            wire[i,1] -= 1
            if hash(tuple(np.array( [tcp[0] + wire[i,1]  , tcp[1] + wire[i,0]  ]) )) not in self.targets:
                self.targets.append(hash(tuple(np.array( [tcp[0] + wire[i,1] , tcp[1] + wire[i,0] ]) )))
                self.target_tcp = np.array([tcp[0] + wire[i,1] , tcp[1] + wire[i,0] ])
                # print("new target: ",self.target_tcp)
                # print("current tcp: ", tcp)
                break
        
    def lin_reg(self, indexes):
            
            # x matrix
            x_m = np.ones((2, len(indexes[1])))

            # sort the point in ascending order,
            # as a rule use the distance from 0,0
            to_dist = np.array([0.0, 0.0])

            xy = np.ones((2, len(indexes[1])))
            xy[0] = np.array(indexes[1])
            xy[1] = np.array(indexes[0])
            xy = xy.transpose() 
                    
            dist = np.linalg.norm( xy - to_dist, axis = 1 )
            sort = np.argsort(dist)
            xy = xy[sort]

            x_m[1] = np.array(xy.transpose()[0])
            y = np.matrix(xy.transpose()[1])

            indexes = np.asarray(indexes).transpose()
            x_m = np.matrix(x_m.transpose())

            # optimal theta
            theta_v = np.linalg.pinv(x_m) * y.transpose()

            return theta_v

    def collision(self, state, thickenning = True):
        
        collision = False

        # look for electodes
        indexes_el  = np.where(state.get_state()[1] == 1)
        indexes_el = np.asarray(indexes_el).transpose()

        # take the wire from the state
        wire = state.get_state()[0]
        # do thickenning with 3x3 rectangle
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        wire = cv2.dilate(wire, kernel)

        # see if any of the electrods colide with
        # the thickend wire
        for index in indexes_el:
            if wire[index[0],index[1]] == 1:
                collision = True
                break
           
        if collision:
            pass
        else:
            # look for wire
            indexes_wire  = np.where(state.get_state()[0] == 1)
            theta_v = self.lin_reg(indexes_wire)
            diff = 0 
            for el in indexes_el:
                y = theta_v[0] + theta_v[1]*el[1] 
                #print(y)
                if el[0] > y:
                    diff += 1
                elif el[0] < y:
                    diff -= 1
            if diff == 2 or diff == -2:
                collision = True
                time.sleep(1)

        if state.get_tcp_xy()[0] < 18:
            collision = True

        return collision

    def angle(self,state):

        scaling = -1

        angle = state.get_orientation()# - 90

        tcp = state.get_tcp_xy()
        a = 5
        b = 6
        temp = self.img[ tcp[1]-a : tcp[1]+b , tcp[0]-a : tcp[0]+b ]

        wire  = np.where(temp == 1)
        if len(wire[0]) < 3:
            return scaling
        
        wire_t = np.asarray(wire).transpose()
        
        x = wire_t[:,1]
        t = x[0]
        flag = False
        for i in x:
            if abs(t-i) > 1:
                flag = True

        if flag:
            theta = self.lin_reg(wire)
            print("Theta",theta)

        if True:

            if flag:
                tan_ = atan2(theta[1],1)* 180 / pi
            else:        
                tan_ = 90

            print("Tan: ", tan_)
            print("ORi: ", angle)

            if angle*tan_ > 0:
                angle = abs(angle+tan_)
            else:
                angle = abs(angle-tan_)

            print("Diff", angle)

            if angle > 60 and angle < 120:
                scaling = 1
        
        else:
            scaling = 1

        return scaling

    def distance_to_target(self,state):

        tcp = state.get_tcp_xy()
        dist = np.array( [ tcp[0]-self.target_tcp[0],tcp[1]-self.target_tcp[1] ] )
        dist = np.linalg.norm(dist)

        return dist

    def get_reward(self, state, action):

        reward = 0
        itr = False
        col = self.collision(state)
        #angle = self.angle(state)
        dist = self.distance_to_target(state)

        if col:
            reward += rewards.COLLISION.value*self.counter
            self.counter = 0

        else: 
            # if angle == 1:
            #     reward += self.counter*rewards.NO_PROGRESS.value*self.max_iterrations/self.counter
            tcp = state.get_tcp_xy()
            if tcp[0] == self.target_tcp[0] and tcp[1] == self.target_tcp[1]:
                self.tcp_on_target = True
                reward += rewards.PASSED.value * self.max_iterrations/self.counter
                self.counter = 0

            else:
                reward += rewards.NO_PROGRESS.value
                if action < Motions.c.value:
                    if dist > self.dist:
                        reward = -reward 
                    else:
                        reward = reward /self.dist
                        self.dist = dist
                else:
                    pass
                
                if self.counter >= self.max_iterrations:
                    itr = True 

        return reward, col, itr

    def action_nr_to_vector(self,action_nr):

        print("Action: " , Motions(action_nr).name)
        action_vector = np.zeros(3)

        if Motions(action_nr).name == "u":

            action_vector[1] -= 1

        elif Motions(action_nr).name == "d":

            action_vector[1] += 1

        elif Motions(action_nr).name == "l":

            action_vector[0] -= 1


        elif Motions(action_nr).name == "r":

            action_vector[0] += 1


        elif Motions(action_nr).name == "c":

            action_vector[2] -= 45

        elif Motions(action_nr).name == "w":

            action_vector[2] += 45

        return action_vector

    def get_last_legit_state(self):
        return self.last_legit_state

