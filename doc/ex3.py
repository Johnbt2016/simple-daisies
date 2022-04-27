import pydaisi as pyd
import time

d = pyd.Daisi("Sleeping Daisi", base_url = "https://dev3.daisi.io")

def compute():
    start = time.time()
    a = d.long_wait(1)
    return time.time() - start
