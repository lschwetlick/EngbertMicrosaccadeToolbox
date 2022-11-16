import numpy as np
from EngbertMicrosaccadeToolbox import microsac_detection

"""This is a set of legacy tests, to ensure the exact numerical result is the
same in the R version and in the python version. These tests rely on data files
obtained by running the R version of the code.
"""


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


def test_test_crit():
    input_array = np.load("tests/xr.npy")
    v = microsac_detection.vecvel(input_array, sampling=500)
    test, radius = microsac_detection._test_crit(v, VFAC=5)
    expected = np.genfromtxt("tests/xrs_criterion.dat")
    assert np.allclose(expected, test)


def test_identify_saccade_candidates():
    input_array = np.load("tests/xr.npy")
    v = microsac_detection.vecvel(input_array, sampling=500)
    test, radius = microsac_detection._test_crit(v, VFAC=5)
    indx = np.where(test > 1)[0]
    sac = microsac_detection._identify_saccade_candidates(indx, 3)
    expected = np.genfromtxt("tests/sac_cand.dat")[:, 0:2]
    # all indexes are off by 1, because python is 0 indexed
    assert np.allclose(expected - 1, np.array(sac))


def test_microsac():
    input_array = np.load("tests/xr.npy")
    sac = microsac_detection.microsacc(input_array)
    expected = np.genfromtxt("tests/xrs_sac.dat")
    res = np.array(sac)
    #offbyone
    res[:, 0:2] = res[:, 0:2] + 1
    print(res)
    assert np.allclose(expected[:, 0:5], res)