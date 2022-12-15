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
    sac, radius = microsac_detection.microsacc(input_array)
    expected = np.genfromtxt("tests/xrs_sac.dat")
    res = np.array(sac)
    # offbyone
    res[:, 0:2] = res[:, 0:2] + 1
    np.testing.assert_allclose(expected[:, 0:7], res)


def test_mark_combined():
    input_array_l = np.genfromtxt("tests/sacl.dat")
    input_array_r = np.genfromtxt("tests/sacr.dat")
    input_array_l[:, 0:2] = input_array_l[:, 0:2] - 1
    input_array_r[:, 0:2] = input_array_r[:, 0:2] - 1
    s = microsac_detection._mark_combined_sacs(input_array_r, input_array_l)
    expected = np.genfromtxt("tests/s.dat")
    np.testing.assert_allclose(expected, s)


def test_binsacc():
    input_array_l = np.genfromtxt("tests/sacl.dat")
    input_array_r = np.genfromtxt("tests/sacr.dat")
    input_array_l[:, 0:2] = input_array_l[:, 0:2] - 1
    input_array_r[:, 0:2] = input_array_r[:, 0:2] - 1
    bino, monol, monor = microsac_detection.binsacc(input_array_l, input_array_r)
    expected_bino = np.genfromtxt("tests/bino.dat")
    expected_bino[:, 0:2] = expected_bino[:, 0:2] - 1
    expected_bino[:, 7:9] = expected_bino[:, 7:9] - 1
    expected_monol = np.genfromtxt("tests/monol.dat")
    expected_monol[:, 0:2] = expected_monol[:, 0:2] - 1
    np.testing.assert_allclose(expected_bino, np.array(bino))
    np.testing.assert_allclose(expected_monol, np.array(monol))
    assert monor == []

def test_sacpar():
    input_array = np.genfromtxt("tests/sacpar_in.dat")
    sac = microsac_detection.sacpar(input_array)
    expected = np.genfromtxt("tests/sacpar_out.dat")
    np.testing.assert_allclose(expected, sac)
