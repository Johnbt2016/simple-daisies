import numpy as np

def add_noise(a):
    if len(a.shape) == 2:
        b = np.random.rand(a.shape[0], a.shape[1])
        return a + b
    else:
        return a

def dot_product(a, b):

    if len(a.shape) == 2 and len(b.shape) == 1 and a.shape[1] ==  b.shape[0]:
        return a.dot(b)
    else:
        return "Incompatible dimensions"

if __name__ == "__main__":
    dim = 200
    a = np.eye(dim)
    b = np.ones((dim,))

    res1 = add_noise(a)

    res2 = dot_product(a, b)
    print(res2)
    assert res2.all() == b.all()