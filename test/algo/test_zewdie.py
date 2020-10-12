from dimep.api import zewdie
import numpy as np


def test_zewdie(normtrace):
    trace = np.zeros((2000))
    assert zewdie(trace, 1000) == 0.0
    # does not pass either threshold
    assert zewdie(normtrace, 1000, 1000) == 0.0
    # does not pass 100µV threshold
    normtrace[1000:] = 0
    normtrace[1031] = 49
    assert zewdie(normtrace, 1000, 1000) == 49.0
    assert zewdie(normtrace, 1000, 1000, discernible_only=True) == 0.0
    # pass 100µV threshold
    normtrace[1031] = 25
    normtrace[1050] = -24
    assert zewdie(normtrace, 1000, 1000) == np.ptp(normtrace[1031:1051])
    assert zewdie(normtrace, 1000, 1000, discernible_only=True) == 0.0
    # does pass 100µV but not 3 * SD threshold
    # becuase the first peak deflects by 100
    normtrace[970:1000] *= 100
    assert zewdie(normtrace, 1000, 1000) == 0.0
