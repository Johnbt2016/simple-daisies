import numpy as np

def stack_arrays(a, b):
    # a, b are 1D numpy arrays

    a += 1
    b += 2

    return np.vstack((a, b))



    