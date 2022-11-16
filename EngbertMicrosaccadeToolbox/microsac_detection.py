import numpy as np


def pix2deg(pix, moWidthPX, moWidthCM, distanceCM):
    """ Converts a given number of pixels to degrees of visual angle

    Parameters
    ----------
    pix : np.array
        the array of pixels you want to convert to degrees
    moWidthPX : int
        number of pixels that the monitor has in the horizontal axis
    moWidthCM : float
        width of the monitor in centimeters
    distanceCM : _type_
       the
    distance of the monitor to the retina

    Returns
    -------
    np.array
        array of degrees
    """
    degPerCm = np.arctan2(1, distanceCM) * 180 / np.pi
    pxPerCm = moWidthPX / moWidthCM
    degPerPx = degPerCm / pxPerCm
    deg = degPerPx * pix
    return deg


def vecvel(x, sampling):
    """Compute velocity times series from position data

    Parameters
    ----------
    x : np.array
        of shape (N, 2)
    sampling : int
        sampling rate

    Returns
    -------
    np.array
        of velocities
    """
    N, _ = x.shape
    v = np.zeros((N, 2))
    print(v.shape)
    v[2:(N - 2), ] = sampling / 6 * (x[4:N, ] + x[3:(N - 1), ]
                                     - x[1:(N - 3), ] - x[0:(N - 4), ])
    v[1, ] = sampling / 2 * (x[2, ] - x[0, ])
    v[(N - 2), ] = sampling / 2 * (x[N - 1, ] - x[(N - 3), ])
    return v


def smoothdata(x):
    x0 = x[0, ]
    v = vecvel(x, sampling=1)
    v[0, ] = v[0, ] + x0
    v = v.cumsum(axis=0)
    return v

    
    
    




def microsacc():
    raise Exception("Not Implemented")



def binsacc():
    raise Exception("Not Implemented")



def aaft():
    raise Exception("Not Implemented")


def boxcount():
    raise Exception("Not Implemented")

def ffth():
    raise Exception("Not Implemented")

def ftpr():
    raise Exception("Not Implemented")

def ifftsh():
    raise Exception("Not Implemented")

def lagdist():
    raise Exception("Not Implemented")



def sacpar():
    raise Exception("Not Implemented")

def surrogate():
    raise Exception("Not Implemented")
