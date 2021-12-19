import math
import numpy
import matplotlib.pyplot as plt

PI = math.pi


def fourier_coeffs(function, N):
    # input function = [f(-pi),f(-pi+eplison)...,f(pi)]
    # input n = how many functions in the interpolation
    # output - first 2n fourier coefficients

    jump_size = 2 * math.pi / (len(function) - 1)

    cos_coeffs = []
    sin_coeffs = []
    for k in range(0, N+1):
        ak = sum(math.cos(k*(-PI+i*jump_size))*function[i] for i in range(len(function)))
        cos_coeffs.append(ak/PI)
        bk = sum(math.sin(k * (-PI + i * jump_size)) * function[i] for i in range(len(function)))
        sin_coeffs.append(bk/PI)
    return cos_coeffs, sin_coeffs


def fourier_sum(function, N):
    # input series of fourier coefficients
    # output - list of fourier series points

    coeffs = fourier_coeffs(function, N)
    length = len(function)       #  = fourier_result[2] -- used to be function
    jump_size = 2 * PI / length
    res = [sum(coeffs[0][i] * math.cos(i * (-PI + k * jump_size)) * jump_size * (length+1) / (length * ((i==0)+1)) + coeffs[1][i] * math.sin(
        i * (-PI + k * jump_size)) * jump_size * (length+1)/ length  for i in range(N)) for k in range(length)]
    return res


def graph_function(vals, ax, colour="black"):
    # vals : a list of (x, f(x))

    xs = numpy.arange(-math.pi, math.pi, 2 * math.pi / len(vals))
    ax.plot(xs, vals, color=colour)

