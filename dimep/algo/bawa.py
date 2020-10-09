"""

Bawa, P., J.D. Hamm, P. Dhillon, and P.A. Gross. “Bilateral Responses of Upper Limb Muscles to Transcranial Magnetic Stimulation in Human Subjects.” Experimental Brain Research 158, no. 3 (October 2004). https://doi.org/10.1007/s00221-004-2031-x.

"For each condition and each muscle, unrectified EMG was averaged, and peak-to-peak values of MEPs were measured for the ipsilateral and the contralateral responses"    
"""
import numpy as np
from numpy import ndarray, inf
from typing import Tuple
from math import ceil


def bawa(
    trace: ndarray,
    tms_sampleidx: int,
    fs: float = 1000,
    mep_window_in_ms: Tuple[float, float] = (0, inf),
):
    """Estimate the amplitude of an iMEP based on Bawa 2004

    Calculates the PtP-Amplitude of the unrectified EMG from 

    args
    ----
    trace:ndarray
        the onedimensional EMG signal
    tms_sampleidx: int
        the sample at which the TMS pulse was applied
    fs:float
        the sampling rate of the signal
    mep_window_in_ms: Tuple[float, float]
        the search window after TMS to look for an iMEP. The manuscript did not specify a restricted search window, and by default we search the whole trace, starting from the TMS to the end of the supplied samples.

    returns
    -------
    amplitude:float
        the peak-to-peak iMEP amplitude of the unrectified EMG after TMS
    

    .. admonition:: Reference

        Bawa, P., J.D. Hamm, P. Dhillon, and P.A. Gross. “Bilateral Responses of Upper Limb Muscles to Transcranial Magnetic Stimulation in Human Subjects.” Experimental Brain Research 158, no. 3 (October 2004). https://doi.org/10.1007/s00221-004-2031-x.


    .. seealso::

        :func:`~.odergreen` also takes the PtP amplitude, but only if it passes a threshold

    """
    a = tms_sampleidx + ceil(mep_window_in_ms[0] * fs / 1000)
    # b should not be higher then the len of the trace
    b = ceil(
        min((tms_sampleidx + (mep_window_in_ms[1] * fs / 1000)), len(trace))
    )
    return np.ptp(trace[a:b])

