"""
Responses in the muscle ipsilateral to cortical stimula-tion were analyzed in the two tasks in which the ipsilateralmuscle was activated during stimulation (ipsilateral activa-tion, bilateral activation). The number of stimuli that gaverise to a discernable ipsilateral MEP (iMEP; 10–30 ms onset, >100µV) was recorded for all stimulus intensitiesand converted to a percentage of total stimuli given.
"""
from numpy import ndarray
from typing import Tuple
from math import ceil
from dimep.tools import bw_boundaries
import numpy as np


def lewis(trace: ndarray, tms_sampleidx: int, fs: float = 1000,) -> bool:
    """Estimate iMEP onset and offset based on Chen 2003
    args
    ----
    trace:ndarray
        the onedimensional EMG signal
    tms_sampleidx: int
        the sample at which the TMS pulse was applied
    fs:float
        the sampling rate of the signal

    returns
    -------
    iMEPOccurence: bool
        whether an iMEP was present or not

    """
    return False
