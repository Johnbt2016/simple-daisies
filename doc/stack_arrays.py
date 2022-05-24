#Comment line
import numpy as np


# A class definition. No endpoints are created for the methods of the class
class Stack:
    def __init__(self, nx):
        self.stack = np.zeros((1,nx))
        self.nb_layers = self.stack.shape[0]

    def stack_arrays(self, ar):
        self.stack += 1
        self.stack = np.vstack((self.stack, ar))
        self.nb_layers = self.stack.shape[0]

# A function, for which an endpoint is created
def compute(stack, ar):

    print(ar)
    stack.stack_arrays(ar)
    return stack

if __name__ == "__main__":
    nx=100
    s = Stack(nx)
    for i in range(8):
        s.stack_arrays(np.random.rand(nx,))

    # Invoke the "compute()" endpoint, add a new layer to the stack 
    # and receive back the updated Stack object
    d_execution = daisi_serialize.compute(stack=s, ar=np.random.rand(nx,)).value

    print(d_execution)