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

    if nsac > 0:
        # Compute peak velocity, horiztonal and vertical components
        for i, s in enumerate(sac):
            # Onset and offset for saccades
            start = int(s[0])
            end = int(s[1])

            # Saccade peak velocity (vpeak)
            vpeak = np.max(np.sqrt(v[start:end, 0]**2 + v[start:end, 1]**2))
            # Saccade vector (dx,dy)
            dx = x[end, 0] - x[start, 0]
            dy = x[end, 1] - x[start, 1]

            # Saccade amplitude (dX,dY)

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
            sac_prop = [start, end, vpeak, dx, dy, x_amp, y_amp]
            sac_list.append(sac_prop)
            # in theory also the radius
    return(sac_list, radius)


def _mark_combined_sacs(ixes_r, ixes_l):
    # Determine saccade clusters
    end_ixes_l = ixes_l[:, 1]  # [s[1] for s in sacl]
    end_ixes_r = ixes_r[:, 1]  # [s[1] for s in sacr]
    TR = np.max(end_ixes_r)
    TL = np.max(end_ixes_l)
    TB = int(np.max([TL, TR]))
    sacs = np.zeros(TB + 2)

    for sl in ixes_l:
        sacs[int(sl[0]):(int(sl[1]) + 1)] = 1

    for sr in ixes_r:
        sacs[int(sr[0]): (int(sr[1]) + 1)] = 1
    sacs[0] = 0
    sacs[TB + 1] = 0
    return sacs


def binsacc(sacl, sacr):
    ixes_l = np.array([np.array([s[0], s[1]]) for s in sacl])
    ixes_r = np.array([np.array([s[0], s[1]]) for s in sacr])

    NB = 0
    NR = 0
    NL = 0
    if (len(sacr) != 0) and (len(sacl) != 0):
        s = _mark_combined_sacs(ixes_l, ixes_r)
        # Find onsets and offsets of microsaccades
        onoff = np.where(np.diff(s) != 0)[0]
        m = onoff.reshape((-1, 2))
        N = m.shape[0]

        # Determine binocular saccades
        bino = []
        monol = []
        monor = []
        for i in range(N):
            left = np.where(np.logical_and((m[i, 0] <= ixes_l[:, 0]),
                                           (ixes_l[:, 1] <= m[i, 1])))[0]
            right = np.where(np.logical_and((m[i, 0] <= ixes_r[:, 0]),
                                            (ixes_r[:, 1] <= m[i, 1])))[0]
            # Binocular saccades
            if len(left) > 0 and len(right) > 0:
                ampl = 0
                l_ix = 0
                for il, l in enumerate(left):
                    new_ampl = np.sqrt(sacl[l][5]**2 + sacl[l][6]**2)
                    if new_ampl > ampl:
                        ampl = new_ampl
                        l_ix = il

                ampr = 0
                r_ix = 0
                for ir, r in enumerate(right):
                    new_ampr = np.sqrt(sacr[r][5]**2 + sacr[r][6]**2)
                    if new_ampr > ampr:
                        ampr = new_ampr
                        r_ix = ir
                NB += 1
                combined = list(sacl[left[l_ix]])
                combined.extend(list(sacr[right[r_ix]]))
                bino.append(combined)
            else:
                if len(left) == 0:
                    assert len(right) == 1
                    ampr = np.sqrt(sacr[right[0]][5]**2 + sacr[right[0]][6]**2)
                    NR += 1
            #           ir <- which.max(ampr)
                    monor.append(list(sacr[right[0]]))
                if len(right) == 0:
                    assert len(left) == 1
                    ampl = np.sqrt(sacl[left[0]][5]**2 + sacl[left[0]][6]**2)
                    NL += 1
                    monol.append(list(sacl[left[0]]))
    return bino, monol, monor


def sacpar(sac):
    """calculates characteristic parameters for binocular microsaccades

    Parameters
    ----------
    sac : list or np.array
        binocular saccade tables from binsacc
    

    Returns
    -------
    list or np.array depending on input
        Basic saccade parameters: (1) onset, (2) end, (3) duration, 
                                (4) delay between eyes, (5) peak velocity, (6) distance, 
                                (7) orientation related to distance vector, (8) amplitude, 
                                (9) orientation related to amplitude vector
    """
    conv = False
    if isinstance(sac,list):
        sac = np.array(sac)
        conv = True
    if not sac.size:
        return None
    M = len(sac)

    # Onset
    a = sac[:,[0,7]]
    a = np.array([min(a[i,:]) for i in range(M)])
    
    # Offset
    b = sac[:,[1,8]]
    b = np.array([min(b[i,:]) for i in range(M)])
    
    # Duration
    DR = sac[:,1] - sac[:,0] + 1
    DL = sac[:,8] - sac[:,7] + 1
    D = (DR+DL)/2

    # Delay between eyes
    delay = b-a+1

    # Peak velocity
    vpeak = (sac[:,2] + sac[:,9])/2

    # Saccade distance
    dist = (np.sqrt(sac[:,3]**2+sac[:,4]**2) + np.sqrt(sac[:,10]**2+sac[:,11]**2))/2
    angle = np.arctan2((sac[:,4]+sac[:,11])/2, (sac[:,3]+sac[:,10])/2)

    # Saccde amplitude and angle
    ampl = (np.sqrt(sac[:,5]**2+sac[:,6]**2) + np.sqrt(sac[:,12]**2+sac[:,13]**2))/2
    angle2 = np.arctan2((sac[:,6] + sac[:,13])/2, (sac[:,5]+sac[:,12])/2)

    out = np.stack([a,b,D,delay,vpeak,dist,angle,ampl,angle2]).T

    # if input was list convert back to list
    if conv:
        out = out.tolist()
    return out
