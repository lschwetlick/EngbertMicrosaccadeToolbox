import numpy as np
from EngbertMicrosaccadeToolbox import data_simulation

def load_complex(path):
    with open(path, "r") as file:
        cc = []
        for line in file:
            line = line.strip()
            line = line[:-1]+"j"
            cc.append(complex(line))
    return cc


def test_fftsh():
    input_array = load_complex("tests/fftsh_input.dat")
    expected = load_complex("tests/fftsh_output.dat")
    result = data_simulation.fftsh(input_array)
    assert np.allclose(expected, result)


def test_ifftsh():
    input_array = load_complex("tests/ifftsh_input.dat")
    expected = load_complex("tests/ifftsh_output.dat")
    input_array = np.array(input_array)
    result = data_simulation.ifftsh(input_array)
    assert np.allclose(expected, result)


def test_ftpr_phi1():
    rand = np.genfromtxt("tests/ftpr_rand.dat")
    exp = np.genfromtxt("tests/phi1_output.dat")
    N = 1499
    r = data_simulation._ftpr_phi1(rand, N)
    assert np.allclose(exp, r)


def test_ftpr():
    input_array = np.genfromtxt("tests/ftpr_input.dat")
    rand = np.genfromtxt("tests/ftpr_rand.dat")
    expected = load_complex("tests/ftpr_output.dat")
    expected = np.array(expected)
    result = data_simulation.ftpr(input_array, rand)
    print(expected[0:4])
    print(result[0:4])
    assert np.allclose(expected.real, result.real)