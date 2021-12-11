import math
import numpy

PI = math.pi

def fourierComputer(function, N):
    #input function = [f(-pi),f(-pi+eplison)...,f(pi)]
    #input n = number of coefficients
    #output - fisrt 2n fourier coefficients
    jump_size = 2 * math.pi / (len(function)-1)
    cos_coefs = [ 1/PI * sum( [(math.cos(k *(-PI + i * jump_size)) * function[i]) for i in range(len(function))]) for k in range(N+1)]
    sin_coef = [ 1/PI *sum( [(math.sin(k *(-PI + i * jump_size)) * function[i]) for i in range(len(function))]) for k in range(N+1)]
    return (cos_coefs, sin_coef, len(function))

def fourierDrawer(function, N):
    #input series of fourier coefficients
    #output - list of fourier series points
    fourier_result = fourierComputer(function, N)
    length = fourier_result[2]
    jump_size = 2 * PI / length
    res = [ sum( [fourier_result[0][i] *math.cos(i * (-PI + k * jump_size)) + fourier_result[1][i] *math.sin(i * (-PI + k * jump_size)) for i in range(N+1)]) for k in range(length)]
    return res