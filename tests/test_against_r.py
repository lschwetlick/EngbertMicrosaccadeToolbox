import numpy as np
from EngbertMicrosaccadeToolbox import microsac_detection


def test_smoothdata():
    input_array = np.load("tests/xr.npy")
    expected = np.genfromtxt("tests/xrs_smooth.dat")
    result = microsac_detection.smoothdata(input_array)
    assert np.allclose(expected, result)


def test_vecvel():
    input_array = np.load("tests/xr.npy")
    expected = np.genfromtxt("tests/xrs_vecvel.dat")
    result = microsac_detection.vecvel(input_array, sampling=500)
    assert np.allclose(expected, result)
