from math import *
import numpy


def fourier_coeffs(function, N):
    # input function = [f(-pi),f(-pi+epsilon)...,f(pi)]
    # input n = how many functions in the interpolation
    # output - first 2n fourier coefficients

    jump_size = 2 * pi / (len(function) - 1)

    cos_coeffs = []
    sin_coeffs = []
    for k in range(0, N + 1):
        ak = sum(cos(k * (-pi + i * jump_size)) * function[i] for i in range(len(function)))
        cos_coeffs.append(ak / pi)
        bk = sum(sin(k * (-pi + i * jump_size)) * function[i] for i in range(len(function)))
        sin_coeffs.append(bk / pi)
    return cos_coeffs, sin_coeffs


def fourier_sum(function, N):
    # input series of fourier coefficients
    # output - list of fourier series points

    coeffs = fourier_coeffs(function, N)
    length = len(function)  # = fourier_result[2] -- used to be function
    jump_size = 2 * pi / length
    res = [sum(
        coeffs[0][i] * cos(i * (-pi + k * jump_size)) * jump_size * (length + 1) / (length * ((i == 0) + 1)) +
        coeffs[1][i] * sin(
            i * (-pi + k * jump_size)) * jump_size * (length + 1) / length for i in range(N + 1)) for k in
           range(1, length)]
    return res


def graph_function(vals, ax, colour="black"):
    # vals : a list of (x, f(x))

    xs = numpy.arange(-pi, pi, 2 * pi / len(vals))
    ax.plot(xs, vals, color=colour)
