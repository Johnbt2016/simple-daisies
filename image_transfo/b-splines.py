import numpy as np
from scipy import signal, misc
from copy import deepcopy

def compute_deriv(image = None):

    if image is None:
        image = misc.face(gray=True).astype(np.float32)

    derfilt = np.array([1.0, -2, 1.0], dtype=np.float32)
    ck = signal.cspline2d(image, 8.0)
    deriv = (signal.sepfir2d(ck, derfilt, [1]) +
                signal.sepfir2d(ck, [1], derfilt))

    
    final = deepcopy(deriv)
    final = 1 - final
    threshold = 0.1
    final[final > threshold] = 1
    final[final < threshold] = 0

    return final



