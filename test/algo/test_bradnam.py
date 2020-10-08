from dimep.algo import bradnam
import numpy as np


def test_bradnam():
    trace = np.zeros((2000))
    imep = bradnam(trace, tms_sampleidx=1000, fs=1000)
    assert imep == 0.0
    # does not pass the 5ms threshold
    trace[1010:1014] = 10
    imep = bradnam(trace, tms_sampleidx=1000, fs=1000)
    assert imep == 0.0
    # now it passes the 5ms threshold, but does not lie in the 10-30ms window
    trace[1007:1014] = 10
    imep = bradnam(trace, tms_sampleidx=1000, fs=1000)
    assert imep == 0.0
    # another passes the 5ms threshold, but does not lie in the 10-30ms window
    trace[1027:1034] = 10
    imep = bradnam(trace, tms_sampleidx=1000, fs=1000)
    assert imep == 0.0
    # now above the threshold and within window
    trace[1010:1020] = 5
    imep = bradnam(trace, tms_sampleidx=1000, fs=1000)
    assert imep == 50.0
