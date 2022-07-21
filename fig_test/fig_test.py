import matplotlib.pyplot as plt

def get_fig():
    a = [0,1]
    fig, ax = plt.subplots()
    ax.plot(a, a)

    return fig
