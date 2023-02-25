import numpy as np


def make_data(N):
    x = np.linspace(0, 2*np.pi, N)
    a = np.linspace(0, np.pi, N)
    b = np.linspace(0, np.pi/2, N)
    y = np.zeros_like(x)
    return y, x, a, b
