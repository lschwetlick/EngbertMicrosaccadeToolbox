import numpy as np
from EngbertMicrosaccadeToolbox import microsac_detection
import pytest


@pytest.mark.xfail
def test_pix2deg():
    """tested against r version
    """
    input_array = np.array([1, 2, 3, 4])
    expected = np.array([1, 2, 3, 4])
    result = microsac_detection.pix2deg(input_array, 5, 6, 7)
    assert np.allclose(expected == result).all()


def test_vecvel():
    input_array = np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]).T
    expected = np.array([[0, 500, 500, 500, 0], [0, 500, 500, 500, 0]]).T
    result = microsac_detection.vecvel(input_array, 500)
    assert np.allclose(expected, result)


def test_mark_combined():
    input_array_l = np.array([[1, 3], [6, 9]])
    input_array_r = np.array([[2, 4], [6, 9]])
    s = microsac_detection._mark_combined_sacs(input_array_r, input_array_l)
    expected = np.array([0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0])
    np.testing.assert_allclose(expected, s.astype(int))
