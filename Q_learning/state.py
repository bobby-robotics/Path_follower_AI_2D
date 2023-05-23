import numpy as np

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
        return hash(tuple(self.current_state.flatten()))
    
    def get_tcp_xy(self) -> np.array:
        return np.array([self.current_state[1][2,2], self.current_state[1][2,3]])
    
    def get_state(self):
        return self.current_state
    
    def set_state(self, new_state):
        self.current_state = new_state