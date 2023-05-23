from enum_motion import Motions
import numpy as np
# from Q_learning.state import state
from math import sin,cos, pi, sqrt
import cv2
from cv2 import WINDOW_NORMAL
import copy
import time

class enviroment():

    img = None
    known_tcp_pose = []
    #last_tcp_pose = None
    #state_cl = None
    img_2 = None
    last_legit_state = None


    def __init__(self, img, initial_tcp) -> None:
        
        self.img = img

        #self.last_tcp_pose = initial_tcp

        #state = state_cl
        self.img_2 = cv2.cvtColor(self.img*255, cv2.COLOR_GRAY2BGR)

        cv2.namedWindow('tcp', WINDOW_NORMAL)
        cv2.resizeWindow('tcp', 400,400)

        cv2.namedWindow('wire', WINDOW_NORMAL)
        cv2.resizeWindow('wire', 400,400)

        cv2.namedWindow('img', WINDOW_NORMAL)
        cv2.resizeWindow('img', 1280,720)
        
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

        #print(indexes)

        # if only 2 found it's all good
        if len(indexes) == 2:
            pos1 = np.array([indexes[0][1], indexes[0][0]])
            temp_state[1][pos1[1],pos1[0]] = 0
            pos1[0] -= 2
            pos1[1] -= 2
        
            pos2 = np.array([indexes[1][1], indexes[1][0]])
            temp_state[1][pos2[1],pos2[0]] = 0
            pos2[0] -=2
            pos2[1] -=2
            
            

        else:
            print(temp_state[1])
            raise Exception("Found more than 2 Electrodes! Not Possible")
        
        #Transform 

        if 1 in np.absolute(pos1):
            pos1 = pos1*sqrt(2)

        if 1 in np.absolute(pos2):
            pos2 = pos2*sqrt(2)

        pos1 = np.matmul(rot,pos1)
        pos2 = np.matmul(rot,pos2)

        # print(pos1)
        # print(pos2)

        pos1 = (pos1).astype("int") 
        pos1[0] += 2
        pos1[1] += 2

        pos2 = (pos2).astype("int")
        pos2[0] += 2
        pos2[1] += 2

        # print(pos1)
        # print(pos2)

        temp_state[1][pos1[1],pos1[0]] = 1
        temp_state[1][pos2[1],pos2[0]] = 1

        # print(temp_state)

        return temp_state

    def update_state(self, action_nr, state, visualise):
        
        self.last_legit_state = copy.deepcopy(state.get_state())

        action_vector = self.action_nr_to_vector(action_nr)

        temp_state = state.get_state()

        tcp = state.get_tcp_xy()

        tcp[0] += action_vector[0]
        tcp[1] += action_vector[1]

        self.img_2[int(tcp[1]),int(tcp[0])] = (0, 0, 255)

        # cut a 5x5 matrix from the image
        y1 = int(tcp[1] - 2    )  #int(5/2)   
        y2 = int(tcp[1] + 2 + 1)  #int(5/2) +1
        x1 = int(tcp[0] - 2    )  #int(5/2)   
        x2 = int(tcp[0] + 2 + 1)  #int(5/2) +1 
           
        temp_state[0] = self.img[y1:y2, x1:x2]

        temp_state[1][2,2] += action_vector[0]
        temp_state[1][2,3] += action_vector[1] 

        temp_state = self.rotate_translate(temp_state, action_vector[2])

        if visualise:
            cv2.imshow("wire", state.get_state()[0])
            cv2.imshow("tcp", state.get_state()[1])
            cv2.imshow("img",self.img_2)
            cv2.waitKey(20)

        return copy.copy(temp_state)
           
    def collision(self, state):
        
        collision = False

        # look for electodes
        indexes_el  = np.where(state.get_state()[1] == 1)
        indexes_el = np.asarray(indexes_el).transpose()

        # look for wire
        # indexes_wire  = np.where(state.get_state()[0] == 1)
        # indexes_wire = np.asarray(indexes_wire).transpose()
        #print("index Wire\n",indexes_wire)
        

        # for index in indexes_el:
        #     if index in indexes_wire:
        #         print(index, "\n",indexes_wire)
        #         #time.sleep(3)
        #         colision = True
        #         break

        
        # for index in indexes_el:
        #     for index_w in indexes_wire:
        #         if np.array_equal(index, index_w):
        #             print(index, "\n",index_w)
        #             #time.sleep(3)
        #             colision = True
        #             break

        for index in indexes_el:
            #print(state.get_state()[0][index[0],index[1]])
            if state.get_state()[0][index[0],index[1]] == 1:
                collision = True
                break
            
        # print(state.get_state()[0], "\n", indexes_el)
        # time.sleep(3)

        return collision

    def get_reward(self, state):

        reward = 0
        
        col = self.collision(state)

        wire_det = False

        wire = np.where(state.get_state()[0])
        wire = np.asarray(wire).transpose()

        if len(wire) < 4:
            print("No Wire There!")
            wire_det = False
            reward -= 50

        elif col:
            reward -= 10

        else: 
            reward += 10

        tcp_x, tcp_y = state.get_tcp_xy()

        # if tcp_x == self.last_tcp_pose[0] and tcp_y == self.last_tcp_pose[1]:
        #     reward +=1

        # else:
        #     temp_tcp = np.array([tcp_x,tcp_y])

        #     if temp_tcp in self.known_tcp_pose:
        #         reward -= 5
        #         if np.array(self.last_tcp_pose) not in self.known_tcp_pose:
        #             self.known_tcp_pose.append(self.last_tcp_pose)

        #         self.last_tcp_pose = np.array(tcp_x,tcp_y)

        if tcp_x < 5 or tcp_x > self.img.shape[1]-5:
            reward -= 1000
            col = True

        if tcp_y < 5 or tcp_y > self.img.shape[0]-5:
            reward -= 1000
            col = True

        return reward, col , wire_det

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


        elif Motions(action_nr).name == "w":

            action_vector[2] -= 45

        elif Motions(action_nr).name == "c":

            action_vector[2] += 45

        

        return action_vector

    def get_last_legit_state(self):
        return self.last_legit_state

