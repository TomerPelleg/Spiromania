import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from math import *

from FourierInterpolation import *
matplotlib.use('TkAgg')


fig, ax = plt.subplots()


def display(func):

    def update_drawing(N):
        N = int(N)
        resu = fourier_sum(func, N)
        ax.cla()
        xs = numpy.arange(-pi, pi, 2 * pi / len(resu))
        ax.plot(xs, func[1:], color="blue")
        ax.plot(xs, resu, color="red")
        fig.canvas.draw_idle()

    res = fourier_sum(func, 2)
    graph_function(res, ax, "red")
    graph_function(func, ax, "blue")
    plt.subplots_adjust(left=0.25, bottom=0.25)

    # Make a horizontal slider to control the frequency.
    axfreq = plt.axes([0.25, 0.1, 0.65, 0.03])
    init_N = 5
    freq_slider = Slider(
        valfmt='%i',
        valstep=1,
        ax=axfreq,
        label='coefficients',
        valmin=1,
        valmax=100,
        valinit=init_N,
    )
    freq_slider.on_changed(update_drawing)
    plt.show()
