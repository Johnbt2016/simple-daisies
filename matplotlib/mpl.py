import matplotlib.pyplot as plt
import numpy as np

def get_fig(nb = 200):
    data = np.random.rand(nb,2)
    fig, ax = plt.subplots()

    ax.scatter(data[:,0], data[:,1])

    return fig

if __name__ == "__main__":
    f = get_fig(1000)
    plt.show()