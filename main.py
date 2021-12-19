from Display import *
import numpy as np
import math


def main():

    func = [ 3*x**2+2 for x in np.arange(-math.pi, math.pi, 0.001)]
    Display(func)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

