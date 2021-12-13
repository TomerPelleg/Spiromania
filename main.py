from FourierInterpolation import *
import numpy as np
import math


def main():
    func = [math.exp(x) for x in np.arange(-math.pi, math.pi, 0.1)]
    res = fourier_sum(func, 5)
    graph_function(res)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

