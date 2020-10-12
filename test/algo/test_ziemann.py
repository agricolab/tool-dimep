from dimep.api import ziemann
import numpy as np


def test_ziemann(normtrace):

    trace = np.zeros((2000))
    assert ziemann(trace, 1000) == 0.0

    # does not pass 1S threshold
    normtrace[950:] = 0.0
    assert ziemann(normtrace, 1000) == 0.0
    # does not pass 5ms threshold
    normtrace[1031] = 49
    assert ziemann(normtrace, 1000, 1000) == 0.0
    # does  pass 5ms threshold
    normtrace[1030:1035] = 25
    assert ziemann(normtrace, 1000, 1000) == 25.0 * 5
    # difference to baseline
    normtrace[:1000] = 5
    assert ziemann(normtrace, 1000, 1000) == 20.0 * 5
    # difference in duration
    normtrace[1030:1045] = 25
    assert ziemann(normtrace, 1000, 1000) == 20.0 * 15
