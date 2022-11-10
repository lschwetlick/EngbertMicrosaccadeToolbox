import numpy as np
from engbert_microsaccade_toolbox import microsac_detection

def test_pix2deg():
    """tested against r version
    """
    input_array = np.array([1, 2, 3, 4])
    expected = np.array([1, 2, 3, 4])
    result = microsac_detection.pix2deg(input_array, 5, 6, 7)
    assert np.allclose(expected == result).all()