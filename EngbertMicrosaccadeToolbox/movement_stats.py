import numpy as np


def boxcount(xx, dx):
    x, y = xx[:, 0], xx[:, 1]
    x_min, y_min = min(x), min(y)
    x_max, y_max = max(x), max(y)
    MX = np.floor((x_max - x_min) / dx).astype(int) + 1
    MY = np.floor((y_max - y_min) / dx).astype(int) + 1
    boxes = np.zeros((MX, MY))
    M = len(x)

    for l_ix in range(M):
        i = np.floor((x[l_ix] - x_min) / dx).astype(int)
        j = np.floor((y[l_ix] - y_min) / dx).astype(int)
        boxes[i, j] = boxes[i, j] + 1
    d = len(np.where(boxes > 0)[0])
    return d


def lagdist(x):
    N = len(x)
    maxlag = round(N / 4)
    x1, x2 = x, x
    r = np.zeros(maxlag)

    for lag in range(maxlag):
        x1 = x1[1:, ]
        x2 = x2[:-1, ]
        d = x1 - x2
        r[lag] = np.mean(d[:, 0]**2 + d[:, 1]**2)

    lag = np.arange(maxlag) + 1
    rv = np.array([lag, r]).transpose()
    return rv
