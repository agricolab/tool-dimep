from dimep.algo import odergren
import numpy as np


def test_odergren():
    trace = np.zeros(2000)
    assert odergren(trace, 1000) == 0.0
    trace[1001] = 99
    assert odergren(trace, 1000) == 0.0
    trace[1002] = -1
    assert odergren(trace, 1000) == 100.0
