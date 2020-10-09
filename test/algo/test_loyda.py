from dimep.algo import loyda
import numpy as np


def test_loyda():
    trace = np.zeros(2000)
    assert loyda(trace, tms_sampleidx=1000, fs=1000) == 0
    trace[1010:1020] = 1
    # shamArea is in average 0, default to 1 -> 100%
    assert loyda(trace, tms_sampleidx=1000, fs=1000) == 100
    trace[980:990] = 0.5
    # divide by shamArea, which is in average 0.5 -> 200%
    assert loyda(trace, tms_sampleidx=1000, fs=1000) == 200.0
    sham_trace = np.ones(2000)
    assert (
        loyda(trace, tms_sampleidx=1000, fs=1000, sham_trace=sham_trace)
        == 100.0
    )

    sham_trace = np.ones(2000) * 0.5
    assert (
        loyda(trace, tms_sampleidx=1000, fs=1000, sham_trace=sham_trace)
        == 200.0
    )
