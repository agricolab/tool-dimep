"""

Bawa, P., J.D. Hamm, P. Dhillon, and P.A. Gross. “Bilateral Responses of Upper Limb Muscles to Transcranial Magnetic Stimulation in Human Subjects.” Experimental Brain Research 158, no. 3 (October 2004). https://doi.org/10.1007/s00221-004-2031-x.

"For each condition and each muscle, unrectified EMG was averaged, and peak-to-peak values of MEPs were measured for the ipsilateral and the contralateral responses"    
"""
import numpy as np
from numpy import ndarray
from typing import Tuple
from math import ceil


def bawa(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 50),
    fs: float = 1000,
):
    """Estimate the amplitude of an iMEP

    based on

    Bawa, P., J.D. Hamm, P. Dhillon, and P.A. Gross. “Bilateral Responses of Upper Limb Muscles to Transcranial Magnetic Stimulation in Human Subjects.” Experimental Brain Research 158, no. 3 (October 2004). https://doi.org/10.1007/s00221-004-2031-x.

    """
    a = tms_sampleidx + ceil(mep_window_in_ms[0] * fs / 1000)
    b = tms_sampleidx + ceil(mep_window_in_ms[1] * fs / 1000)
    if np.ndim(trace) == 1:
        return np.ptp(trace[a:b], 0)
    else:
        raise ValueError("Unclear dimensionality of the trace ndarray")
