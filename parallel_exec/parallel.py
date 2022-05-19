import numpy as np
import time

def apply_chunk(data_chunk, size=10000):
    curve_x = np.arange(size) 
    curve_y = 100*np.random.rand(size,)

    res = [np.interp(data_point, curve_x, curve_y) for data_point in data_chunk]

    return res

def apply_func(data_point, size=10000):
    curve_x = np.arange(size) 
    curve_y = 100*np.random.rand(size,)

    res = np.interp(data_point, curve_x, curve_y)

    return res

if __name__ == "__main__":
    data_size = 100000
    data = 100 * np.random.rand(data_size,)
    start = time.time()
    res = np.array([apply_func(d) for d in data])
    print(time.time() - start)
    # print(res)