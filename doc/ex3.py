import pydaisi as pyd
import time

d = pyd.Daisi("Sleeping Daisi")

def compute():
    start = time.time()
    a = d.long_wait(1)
    return time.time() - start
