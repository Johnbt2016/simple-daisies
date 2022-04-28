from sys import stderr, stdout
from re import compile
import time
import numpy as np

def linpack():
    start = time.time()
    filename = "linpack.out"
    fpnum = r'\d+\.\d+E[+-]\d\d'
    fpnum_1 = fpnum + r' +'
    pattern = compile(r'^ *' + fpnum_1 + fpnum_1 + fpnum_1 + \
        r'(' + fpnum + r') +' + fpnum_1 + fpnum + r' *\n$')
    speeds = [0.0,1.0e75,0.0]

    file = open(filename)
    count = 0
    while file :
        line = file.readline()
        if not line :
            break
        if pattern.match(line) :
            count = count+1
            x = float(pattern.sub(r'\1',line))
            if x < 1.0 :
                print(count)
            speeds[0] = speeds[0]+x
            speeds[1] = min(speeds[1],x)
            speeds[2] = max(speeds[2],x)
    file.close()
    if count != 0 :
        speeds[0] = speeds[0]/count

    return "%6.1f MFlops (%d from %.1f to %.1f) Time: %s seconds\n" % \
        (speeds[0],count,speeds[1],speeds[2], time.time() - start)


def linpack2(n):
    A = np.random.rand(n,n)
    b = np.random.rand(n,1)
    start = time.time()
    solve = np.linalg.solve(A, b)
    stop = time.time()

    op = int(2*n*n*n/3)
    ops = 1e-6 * op / (stop - start)

    return op, stop - start, ops
    



if __name__ == "__main__":
    res = linpack2(3000)
    print(res)
