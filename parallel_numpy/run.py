from pydaisi import Daisi
import numpy as np
import time
import myfunc

my_daisi = Daisi("Numpy Parallel Dev3", base_url = "https://dev3.daisi.io")

nb_cells = 1
exp_oil = 1000 * np.random.rand(nb_cells,)
exp_gas = 200 * np.random.rand(nb_cells,)
vol_to_discount = 100 * np.random.rand(nb_cells,)

start = time.time()
# calls = [my_daisi.discount_losses_(exp_oil=exp_oil[i],exp_gas=exp_gas[i],vol_to_discount=vol_to_discount[i]) for i in range(nb_cells)]
calls = [myfunc.discount_losses(exp_oil=exp_oil[i],exp_gas=exp_gas[i],vol_to_discount=vol_to_discount[i]) for i in range(nb_cells)]


# result = Daisi.run_parallel(*calls)
print(time.time() - start)

print(calls)
