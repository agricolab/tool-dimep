from dimep.api import lewis
import numpy as np


def test_lewis(normtrace):
    trace = np.zeros((2000))
    assert lewis(trace, 1000, 1000) == 0.0
    # does not pass either threshold
    assert lewis(normtrace, 1000, 1000) == 0.0
    # does not pass 100µV threshold
    normtrace[1000:] = 0
    normtrace[1031] = 99
    assert lewis(normtrace, 1000, 1000) == 99.0
    assert lewis(normtrace, 1000, 1000, discernible_only=True) == 0.0
    # pass 100µV threshold
    normtrace[1031] = 100
    normtrace[1050] = -100
    assert lewis(normtrace, 1000, 1000) == np.ptp(normtrace[1031:1051])
    assert lewis(normtrace, 1000, 1000, discernible_only=True) == 0.0
    # does pass 100µV but not 3 * SD threshold
    # becuase the first peak deflects by 100
    normtrace[970:1000] *= 100 / 2
    assert lewis(normtrace, 1000, 1000) == 0.0
