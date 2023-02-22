import numba


@numba.njit
def flop2(y, x, a, b):
    for i in range(y.shape[0]):
        y[i] = a[i] + b[i] + x[i]


@numba.njit
def flop4(y, x, a, b):
    for i in range(y.shape[0]):
        y[i] = a[i] + b[i] + x[i]
        y[i] = a[i] - b[i] - x[i]


@numba.njit
def flop8(y, x, a, b):
    for i in range(y.shape[0]):
        y[i] = a[i] + b[i] + x[i] + a[i] * b[i]
        y[i] = a[i] - b[i] - x[i] * a[i] - b[i]


@numba.njit
def flop16(y, x, a, b):
    for i in range(y.shape[0]):
        y[i] = (a[i] + b[i])*x[i] + a[i]*(x[i] + a[i])*(b[i] - a[i]) + x[i]
        y[i] = (a[i] - b[i])*x[i] - a[i]*(x[i] - a[i])*(b[i] + a[i]) - x[i]


@numba.njit
def flop24(y, x, a, b):
    for i in range(y.shape[0]):
        y[i] = (a[i] + b[i])*x[i] + a[i]*(x[i] + a[i])*(b[i] - a[i]) + x[i]
        y[i] = (a[i] - b[i])*x[i] - a[i]*(x[i] - a[i])*(b[i] + a[i]) - x[i]
        y[i] = (a[i] - b[i])*x[i] - a[i]*(x[i] - a[i])*(b[i] + a[i]) - x[i]


@numba.njit
def flop32(y, x, a, b):
    for i in range(y.shape[0]):
        y[i] = (a[i] + b[i])*x[i] + a[i]*(x[i] + a[i])*(b[i] - a[i]) + x[i]
        y[i] = (a[i] - b[i])*x[i] - a[i]*(x[i] - a[i])*(b[i] + a[i]) - x[i]
        y[i] = (a[i] - b[i])*x[i] - a[i]*(x[i] - a[i])*(b[i] + a[i]) - x[i]
        y[i] = (a[i] + b[i])*x[i] + a[i]*(x[i] - a[i])+(b[i] * a[i]) + x[i]


@numba.njit
def flop64(y, x, a, b):
    for i in range(y.shape[0]):
        y[i] = (a[i] + b[i])*x[i] + a[i]*(x[i] + a[i])*(b[i] - a[i]) + x[i]
        y[i] = (a[i] - b[i])*x[i] - a[i]*(x[i] - a[i])*(b[i] + a[i]) - x[i]
        y[i] = (a[i] - b[i])*x[i] - a[i]*(x[i] - a[i])*(b[i] + a[i]) - x[i]
        y[i] = (a[i] + b[i])*x[i] + a[i]*(x[i] - a[i])+(b[i] * a[i]) + x[i]
        y[i] = (a[i] + b[i])*x[i] + a[i]*(x[i] - a[i])+(b[i] * a[i]) + x[i]
        y[i] = (a[i] + b[i])*x[i] + a[i]*(x[i] + a[i])*(b[i] - a[i]) + x[i]
        y[i] = (a[i] - b[i])*x[i] - a[i]*(x[i] - a[i])*(b[i] + a[i]) - x[i]
        y[i] = (a[i] + b[i])*x[i] + a[i]*(x[i] + a[i])*(b[i] - a[i]) + x[i]
