from dimep.algo import rotenberg
import numpy as np


def test_rotenberg():
    trace = np.zeros(2000)
    assert rotenberg(trace, 1000) == 0.0
    trace[1001] = 1
    assert rotenberg(trace, 1000) == 0.0
    trace[1005] = 1
    assert rotenberg(trace, 1000) == 1.0
    trace[1029] = 1
    assert rotenberg(trace, 1000) == 2.0
    trace[1000:] = 1
    assert rotenberg(trace, 1000) == 25.0
    trace[1000:] = -1
    assert rotenberg(trace, 1000) == 25.0
