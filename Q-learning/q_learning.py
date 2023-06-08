from enum_motion import Motions
import numpy as np

#*************************************
# State definition:
# [tcp_x, tcp_y, orientation]
#
# Agent starting with epsilon value of 1 
# for taking a random action
# gradualy decriesing over time
# wtih value of 0.01 for every episode.
#   
#
#

class q_learning():
    
    img = None

    rewards = None
    transition_probabilities = None
    q_vals = None

    states = None
    actions = None

    intial_state = None
    current_state = None

    epsilon = 1
    delta = 0.01

    reward = 0

    #iterations = 0
    #gamma = 0

    def __init__(self, img) -> None:
        img = img

    def choose_action(self, state):

        if np.random.random() < self.epsilon:

            # if random probability smaller than epsilon 
            # agent should choose a random action     
            return np.random.randint(low = 0, high = len(Motions), size = 1, dtype ="int16")[0]
        
        else:
            # agent is taking a known action
            return 0

    def action_nr_to_vector(self,action_nr):

        action_vector = np.zeros(3)

        if Motions[action_nr] == "r":

            action_vector[0] += 1

        elif Motions[action_nr] == "l":

            action_vector[0] -= 1

        elif Motions[action_nr] == "u":

            action_vector[1] -= 1

        elif Motions[action_nr] == "d":

            action_vector[1] += 1

        elif Motions[action_nr] == "c":

            action_vector[2] -= 45

        elif Motions[action_nr] == "w":

            action_vector[2] += 45

        return action_vector

    def execute_action(self, action_nr):
        
        self.current_state += self.action_nr_to_vector(action_nr)
        
    def reward(self):
        pass
        

    