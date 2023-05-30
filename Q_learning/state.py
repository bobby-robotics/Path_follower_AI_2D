import numpy as np
import copy

# definition of the state is 5x5x2 matrix
# in which the first 5x5 matrix is the 
# cropped part of the image 
# and the second one is np.zeros(5,5)
# with only two points set for the 
# fork and in the middle are the tcp_x and tcp_y 
# coordinates saved


class state():

    current_state = None

    def __init__(self, current_state) -> None:
        self.current_state = current_state

    def __hash__(self) -> int:     
        curr = copy.deepcopy(self.current_state)
        curr[1][2,2:4] = 0
        # curr[1][2,3] = 0   
        # print("hash:",curr)
        return hash(tuple(curr.flatten()))
    
    def get_tcp_xy(self) -> np.array:
        return np.array([self.current_state[1][2,2], self.current_state[1][2,3]])
    
    def get_orientation(self):
        return self.current_state[1][0,4]

    def get_state(self):
        return self.current_state
    
    def set_state(self, new_state):
        self.current_state = new_state