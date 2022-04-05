from pydaisi import Daisi

np_daisi = Daisi("Numpy Tests")

dim = 200
a = np.eye(dim)
b = np.ones((dim,))

res1 = np_daisi.compute(func = "add_noise", a=a)

res2 = np_daisi.compute(func = "dot_product", a=a, b=b)

assert res2.all() == b.all()