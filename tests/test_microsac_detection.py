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
