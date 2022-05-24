# Example from the Daisi documentation

This Daisi receives and send back a custom Python object.

## Example

```python
import pydaisi as pyd
import numpy as np

# Connect to the "Daisi Serialize" Daisi
daisi_serialize = pyd.Daisi("exampledaisies/Daisi Serialize")

# Class definition
class Stack:
    def __init__(self, nx):
        self.stack = np.zeros((1,nx))
        self.nb_layers = self.stack.shape[0]

    def stack_arrays(self, array):
        self.stack += 1
        self.stack = np.vstack((self.stack, array))
        self.nb_layers = self.stack.shape[0]

# Initialize a new GridStack object with 10 layers
nx=100
s = Stack(nx)
for i in range(10):
    s.stack_arrays(np.random.rand(nx,))

# Invoke the "compute()" endpoint, add a new layer to the stack 
# and receive back the updated Stack object
d_execution = daisi_serialize.compute(stack=s, array=np.random.rand(nx,)).value

assert d_execution.nb_layers == 11
```
