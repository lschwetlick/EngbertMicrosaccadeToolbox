import numpy as np
from EngbertMicrosaccadeToolbox import microsac_detection


def aaft(x, random_sequence=None, y1=None):
    N = len(x)
    print(N)
    if np.floor(N / 2) == N / 2:
        x = x[0:N - 1]
        N = N - 1
    x_sorted = np.sort(x)
    x_sorted_index = np.argsort(x)

    if random_sequence is None:
        random_sequence = np.random.normal(size=int(N))
    g_sorted = np.sort(random_sequence)
    # g_sorted_index = np.argsort(g)

    y = random_sequence
    y[x_sorted_index] = g_sorted

    if y1 is None:
        y1 = ftpr(y)
    # y1_sorted = np.sort(y1)
    y1_sorted_index = np.argsort(y1)

    xs = x
    xs[y1_sorted_index] = x_sorted
    return xs


def fftsh(x):
    N = len(x)
    n = int((N - 1) / 2)
    xt = x[n + 1:N + 1]
    xt = np.concatenate((xt, x[0:n + 1]), axis=0)
    return xt


def _ftpr_phi1(random_sequence, N):
    phi0 = np.pi * (2 * random_sequence - 1)
    phi1 = np.zeros(N)
    phi1[:int((N / 2))] = -phi0[::-1]
    phi1[int((N / 2))] = 0
    phi1[int((N / 2)) + 1:] = phi0
    return phi1


def ftpr(x, random_sequence=None):
    N = len(x)
    if np.floor(N / 2) == N / 2:
        x = x[0:N]
        N = N - 1
    x = x - np.mean(x)
    xfft = np.fft.fft(x)
    z0 = fftsh(xfft)

    if random_sequence is None:
        random_sequence = \
            np.random.uniform(low=0, high=1, size=int((N - 1) / 2))

    phi1 = _ftpr_phi1(random_sequence, N)
    z1 = z0 * np.exp(1j * phi1)
    xs = np.fft.ifft(ifftsh(z1), norm="forward") / N
    return xs


def ifftsh(x):
    N = len(x)
    n = (N - 1) / 2
    xt = x[int(n):int(N + 1)]
    xt = np.concatenate((xt, x[0:int(n)]), axis=0)
    return xt


def surrogate(x, SAMPLING):
    x0 = x[0,:]
    v = microsac_detection.vecvel(x,SAMPLING=SAMPLING)
    vsx = aaft(v[:,0])/SAMPLING
