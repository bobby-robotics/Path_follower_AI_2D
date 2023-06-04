import numpy as np
import copy

# definition of the state is 5x5x2 matrix
# in which the first 5x5 matrix is the 
# cropped part of the image 
# and the second one is np.zeros(5,5)
# with two points set for the 
# fork and in the middle are the tcp_x and tcp_y 
# coordinates saved which are used only internaly
# and on the top right corner there is an orientation
# degrees

# Example
# first 5x5 matrix (wire)
#[[[  0.   0.   0.   0.   0.]
#  [  0.   0.   0.   0.   0.]
#  [  1.   1.   0.   0.   0.]
#  [  0.   0.   1.   1.   0.]
#  [  0.   0.   0.   0.   1.]]
#
# second 5x5 matrix ( tool and all
#   infos needed for it)
# [[  0.   0.   0.   0. -45.]
#  [  0.   0.   0.   1.   0.]
#  [  0.   0.  34. 295.   0.]
#  [  0.   1.   0.   0.   0.]
#  [  0.   0.   0.   0.   0.]]]

class state():

    current_state = None

    # self explanatory
    def __init__(self, current_state) -> None:
        self.current_state = current_state

    # hashing fuction that hashes our 5x5x2 matrix 
    # so that we have an unique ID for every state
    # tcp (x,y) are not used/saved for/in the hashing
    # because without it, the state can be used 
    # anywhere on to the image
    def __hash__(self) -> int:     
        curr = copy.deepcopy(self.current_state)
        curr[1][2,2:4] = 0
        return hash(tuple(curr.flatten()))
    
    # self explanatory
    def get_tcp_xy(self) -> np.array:
        return np.array([self.current_state[1][2,2], self.current_state[1][2,3]]).astype(int)
    
    # self explanatory
    def get_orientation(self):
        return self.current_state[1][0,4]

    # self explanatory
    def get_state(self):
        return self.current_state
    
    # self explanatory
    def set_state(self, new_state):
        self.current_state = new_state