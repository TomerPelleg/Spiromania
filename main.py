from Display import *
import numpy as np
from math import *


def main():
    func = [sin(1/exp(x-1)) for x in np.arange(-pi, pi, 0.005)]
    display(func)


if __name__ == '__main__':
    main()
