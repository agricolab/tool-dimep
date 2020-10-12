from dimep.api import wassermann
import numpy as np


def test_wassermann():
    trace = np.zeros((2000))
    assert wassermann(trace, 1000) == 0.0
    trace[1020:1021] = 10
    assert wassermann(trace, 1000) == 0.0
    trace[1020:1022] = 10
    assert wassermann(trace, 1000) == 10.0
    trace[1020:1022] = -10
    assert wassermann(trace, 1000) == 10.0
    # difference in mean area compared to the baseline
    trace[:1000] = 1
    assert wassermann(trace, 1000) == 9.0
