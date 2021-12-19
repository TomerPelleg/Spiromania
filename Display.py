from FourierInterpolation import *
from matplotlib.widgets import Slider, Button
import matplotlib
matplotlib.use('TkAgg')



fig, ax = plt.subplots()



def Display(func):

    def UpdateDraw(N):
        N = int(N)
        res = fourier_sum(func, N)
        ax.cla()
        xs = numpy.arange(-math.pi, math.pi, 2 * math.pi / len(res))
        ax.plot(xs, res, color="red")
        xs1 = numpy.arange(-math.pi, math.pi, 2 * math.pi / len(res))
        ax.plot(xs1, func[1:], color="blue")
        fig.canvas.draw_idle()


    res = fourier_sum(func, 200)
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
        label='N [Num]',
        valmin=1,
        valmax=1000,
        valinit=init_N,
    )
    freq_slider.on_changed(UpdateDraw)
    plt.show()