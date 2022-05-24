import numpy as np

# A class definition. No endpoints are created for the methods of the class
class Stack:
    def __init__(self, nx):
        self.stack = np.zeros((1,nx))
        self.nb_layers = self.stack.shape[0]

    def stack_arrays(self, array):
        self.stack += 1
        self.stack = np.vstack((self.stack, array))
        self.nb_layers = self.stack.shape[0]

# A function, for which an endpoint is created
def compute(stack, array):
    '''
    Parameters:
    - stack (Stack) : a Stack object
    - array (Numpy array) : a Numpy array of shape (nx,)

    Returns:
    - an updated Stack object
    '''
    stack.stack_arrays(array)
    return stack