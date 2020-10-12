from dimep.api import bawa
import numpy as np


def test_bawa():
    trace = np.zeros((2000))
    assert bawa(trace, 1000) == 0
    trace[1002] = 1
    trace[1004] = -1
    assert bawa(trace, 1000) == 2
    assert bawa(trace, 1004) == 1
    assert bawa(trace, 1005) == 0
