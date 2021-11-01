"""Main Access Point for DiMEP Algorithms"""
from dimep.algo import *
from dimep.version import version
from numpy import ndarray
from typing import Dict


def available() -> None:
    "print all available algorithms"
    from dimep.algo import __all__

    for algo in __all__:
        print(algo)


def all(trace: ndarray, tms_sampleidx: int) -> Dict[str, float]:
    """Estimate the iMEP amplitude in the given trace with all implemented algorithms
    
    args
    ----
    trace:ndarray
        the one-dimensional (samples,) EMG signal
    tms_sampleidx: int
        the sample at which the TMS pulse was applied
    

    returns
    -------
    estimtes: Dict[str, float]
        a dictionary of estimates, with the algorithm name as key and the estimate as value
    
    """
    from dimep.algo import __all__

    out = dict()
    for algo in __all__:
        out[str(algo)] = eval(algo)(trace, tms_sampleidx=tms_sampleidx)
    return out
