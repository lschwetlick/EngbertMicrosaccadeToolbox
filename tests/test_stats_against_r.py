import numpy as np
from EngbertMicrosaccadeToolbox import movement_stats

def test_boxcount():
    input_array = np.genfromtxt("tests/boxcount_input.dat")
    expected = np.genfromtxt("tests/boxcount_output.dat")
    dx = 0.01
    result = movement_stats.boxcount(input_array, dx)
    assert np.allclose(expected, result)

def test_lagdist():
    input_array = np.load('tests/xr.npy')
    expected = np.genfromtxt('tests/lagdist_xr_out.dat')
    result = movement_stats.lagdist(input_array)
    assert np.allclose(expected, result)
