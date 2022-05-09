# Signal Processing (scipy.signal) - B splines

This Daisi uses spline-filtering to compute an edge-image (the second derivative of a smoothed spline)
of a raccoon’s face, which is an array returned by the command scipy.misc.face.
The command sepfir2d was used to apply a separable 2-D FIR filter with mirror-symmetric boundary conditions
to the spline coefficients.
This function is ideally-suited for reconstructing samples from spline coefficients
and is faster than convolve2d, which convolves arbitrary 2-D filters and allows for
choosing mirror-symmetric boundary conditions.

```python
import pydaisi as pyd
from scipy import misc
import scipy
import numpy as np
import matplotlib.pyplot as plt

#Step 1 : Load an image and convert to grayscale
face = scipy.misc.face()
plt.gray()
plt.imshow(face)
plt.show()

image = misc.face(gray=True).astype(np.float32)

#Step 2 : call the "Compute B-spline" daisi from your code
b_spline = pyd.Daisi("Compute B-Spline")
deriv = b_spline.compute_deriv(image=image).value

# Step 3 : Visualize the result
import matplotlib.pyplot as plt
plt.imshow(deriv)
plt.show()
```
