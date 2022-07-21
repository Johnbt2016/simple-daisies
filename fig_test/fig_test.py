import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('MacOSX')


def get_fig():
    a = [0,1]
    fig, ax = plt.subplots()
    ax.plot(a, a)

    return fig

def show_figure(fig):

    # create a dummy figure and use its
    # manager to display "fig"  
    dummy = plt.figure()
    new_manager = dummy.canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)

    return fig




if __name__ == "__main__":
    fig = get_fig()

    dummy = plt.figure()
    new_manager = dummy.canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)
    fig.savefig("ttt.png")