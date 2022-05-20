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
    chunk_size = int(data_size / 25)
    data_chunk = [data[i:i+chunk_size] for i in range(25)]
    start = time.time()
    res = np.array([apply_chunk(d, size=1000000) for d in data_chunk])
    print(time.time() - start)
    # print(res)