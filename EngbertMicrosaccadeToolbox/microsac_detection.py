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


def _test_crit(v, VFAC):
    # Compute threshold
    med = np.median(v, axis=0)
    # median square displacement
    msd = np.sqrt(np.median((v - med)**2, axis=0))
    # TODO Warning when too small

    radius = VFAC * msd
    # Apply test criterion: elliptic treshold
    test = ((v / radius)**2).sum(axis=1)
    return test, radius


def _identify_saccade_candidates(indx, mindur):
    """takes an all identified indexes and finds atart and endpoints for
    saccades

    Parameters
    ----------
    indx : np.array
        array of indexes where velocity criterion is met
    mindur : int
        minimum duration of an event

    Returns
    -------
    list
        list of events with [[start, end], ...]
    """
    # Determine saccades
    N = len(indx)
    nsac = 0
    sac = []
    dur = 1
    start = 0
    k = 0
    # Loop over saccade candidates
    while k < N - 1:
        if indx[k + 1] - indx[k] == 1:
            dur += 1
        else:
            # Minimum duration criterion (exception: last saccade)
            if dur >= mindur:
                nsac += 1
                end = k
                sac_prop = [indx[start], indx[end]]
                sac.append(sac_prop)
            start = k + 1
            dur = 1
        k = k + 1

    # Check minimum duration for last microsaccade
    if dur >= mindur:
        nsac = nsac + 1
        end = k
        sac_prop = [indx[start], indx[end]]
        sac.append(sac_prop)
    return sac


def microsacc(x, vfac=5, mindur=3, sampling=500):
    """finds microsaccades

    Parameters
    ----------
    x : np.array
        of shape [N,2] representing positions
    vfac : int
        relative velocity threshold
    mindur : int, optional
        minimal saccade duration
    sampling : int
        sampling rate


    Returns
    -------
    list
        list of events with [(1) onset, (2) end, (3) peak velocity,
                             (4) horizontal component, (5) vertical component,
                             (6) horizontal amplitude, (6) vertical amplitude]
    """
    sac_list = []
    # Compute velocity
    v = vecvel(x, sampling=sampling)

    # Apply test criterion: elliptic treshold
    test, radius = _test_crit(v, vfac)
    indx = np.where(test > 1)[0]

    sac = _identify_saccade_candidates(indx, mindur)
    nsac = len(sac)

    print(nsac)
    if nsac > 0:
        # Compute peak velocity, horiztonal and vertical components
        for i, s in enumerate(sac):
            print(i)
            # Onset and offset for saccades
            start = int(s[0])
            end = int(s[1])

            # Saccade peak velocity (vpeak)
            vpeak = np.max(np.sqrt(v[start:end, 0]**2 + v[start:end, 1]**2))
            # Saccade vector (dx,dy)
            dx = x[end, 0] - x[start, 0]
            dy = x[end, 1] - x[start, 1]

            # Saccade amplitude (dX,dY)
            #print(np.min(x[start:end, 0]))
            #print(x[start:end, 0])

            minx = np.min(x[start:end + 1, 0])
            maxx = np.max(x[start:end + 1, 0])
            miny = np.min(x[start:end + 1, 1])
            maxy = np.max(x[start:end + 1, 1])

            ix1 = np.argmin(x[start:end + 1, 0])
            ix2 = np.argmax(x[start:end + 1, 0])
            iy1 = np.argmin(x[start:end + 1, 1])
            iy2 = np.argmax(x[start:end + 1, 1])

            x_amp = np.sign(ix2 - ix1) * (maxx - minx)
            y_amp = np.sign(iy2 - iy1) * (maxy - miny)
            #print(minx, maxx, miny, maxy, ix1, ix2, iy1, iy2, x_amp, y_amp)
            sac_prop = [start, end, vpeak, dx, dy, x_amp, y_amp]
            sac_list.append(sac_prop)
            # in theory also the radius
    return(sac_list)


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
