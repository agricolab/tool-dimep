from dimep.algo.chen import chen, chen_onoff
import numpy as np


def test_chen():
    trace = np.zeros((2000))
    imep = chen(trace, tms_sampleidx=1000, fs=1000)
    assert imep == 0.0
    # does not pass the 5ms threshold
    trace[1015:1019] = 10
    imep = chen(trace, tms_sampleidx=1000, fs=1000)
    assert imep == 0.0
    # not it passes the 5ms threshold
    trace[1015:1025] = 10
    imep = chen(trace, tms_sampleidx=1000, fs=1000)
    assert imep == 100.0
    # extends the duration to be above mean
    trace[1013:1015] = 5
    trace[1025:1027] = 5
    imep = chen(trace, tms_sampleidx=1000, fs=1000)
    assert imep == 120.0
