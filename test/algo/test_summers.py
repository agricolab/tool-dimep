from dimep.algo import summers
import numpy as np


def test_summers(normtrace):
    trace = np.zeros(2000)
    assert summers(trace, 1000) == 0.0
    trace[1010] = 1
    assert summers(trace, 1000) == 1.0
    assert summers(normtrace, 1000) == 0.0
    # the iMEP is 3 for 10ms
    normtrace[1010:1020] = 3
    # the 10ms before TMS are 0
    normtrace[1000 - 15 : 1000 - 5] = 0
    # the difference in area is 30
    assert summers(normtrace, 1000) == 30.0
    # also if iMEP is negative
    normtrace[1010:1020] = -3
    assert summers(normtrace, 1000) == 30.0
    normtrace[1000 - 15 : 1000 - 5] = -1
    assert summers(normtrace, 1000) == 20.0
