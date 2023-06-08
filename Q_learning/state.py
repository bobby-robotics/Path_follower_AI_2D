import numpy as np
import copy

# definition of the state is 7x7x2 tensor
# in which the first 7x7 matrix is the 
# cropped part of the image 
# and the second one is np.zeros(7,7)
# with two points set for the 
# fork and in the middle are the tcp_x and tcp_y 
# coordinates saved which are used only internaly
# and on the top right corner there is an orientation
# degrees

# Example
# first 7x7 matrix (wire)
#[[[ 0.  0.   0.   0.   0.   0.  0.]
#  [ 1.  0.   0.   0.   0.   0.  0.]
#  [ 0.  1.   0.   0.   0.   0.  0.]
#  [ 0.  1.   1.   0.   0.   0.  0.]
#  [ 0.  0.   0.   1.   1.   0.  0.]
#  [ 0.  0.   0.   0.   0.   1.  0.]
#  [ 0.  0.   0.   0.   0.   1.  0.]]
#
# second 7x7 matrix ( tool and all
#   infos needed for it)
# [[ 0.  0.   0.   0.   0.   0.  45.]
#  [ 0.  0.   0.   0.   0.   1.   0.]
#  [ 0.  0.   0.   0.   0.   0.   0.]
#  [ 0.  0.   0.   34.  295. 0.   0.]
#  [ 0.  0.   0.   0.   0.   0.   0.]
#  [ 0.  1.   0.   0.   0.   0.   0.]
#  [ 0.  0.   0.   0.   0.   0.   0.]]]

class state():

    current_state = None
    middle = None

    # self explanatory
    def __init__(self, current_state) -> None:
        #print(current_state)
        self.current_state = current_state
        self.middle = int(current_state[1].shape[0]/2)
        #print("MIDDLE",self.middle)

    # hashing fuction that hashes our 5x5x2 matrix 
    # so that we have an unique ID for every state
    # tcp (x,y) are not used/saved for/in the hashing
    # because without it, the state can be used 
    # anywhere on to the image
    def __hash__(self) -> int:     
        curr = copy.deepcopy(self.current_state)
        curr[1][self.middle,self.middle:self.middle+2] = 0
        #print("To Hash: ", curr)
        #print(tuple(curr.flatten()))
        return hash(tuple(curr.flatten()))
    
    # self explanatory
    def get_tcp_xy(self) -> np.array:
        return np.array([self.current_state[1][self.middle,self.middle], self.current_state[1][self.middle,self.middle+1]]).astype(int)
    
    # self explanatory
    def get_orientation(self):
        return self.current_state[1][0,2*self.middle]

    # self explanatory
    def get_state(self):
        return self.current_state
    
    # self explanatory
    def set_state(self, new_state):
        self.current_state = new_state