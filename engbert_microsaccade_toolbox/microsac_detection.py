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