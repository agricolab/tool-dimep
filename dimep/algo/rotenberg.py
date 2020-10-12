"""
To eliminate averaging of positive and negative voltages of polyphasic signals, all MEP voltages were converted to absolute values and integrated for measures of power (area under the curve). [...] Peak-to-peak amplitude, motor threshold (MT) and integrated amplitude were computed automatically in the 5–30 msec time window, as our pilot data indicated a 4 msec maximal duration of TMS artifact, and approximately 25 msec maximal latency to onset of the MEP in rats
"""
import numpy as np
from numpy import ndarray
from typing import Tuple
from math import ceil


def rotenberg(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (5, 30),
    fs: float = 1000,
) -> float:
    """Estimate the amplitude of an iMEP based on Rotenberg 2010

    Returns the iMEP Area of the rectified EMG integrated for the search window

    .. warning

        This study was conducted on rats, and therefore the default search window from 5 to 30ms is probably too fast. Consider adapting it when conducting studies with humans, e.g. to 15 to 50ms.
    
    args
    ----
    trace:ndarray
        the onedimensional EMG signal in units of µV
    tms_sampleidx: int
        the sample at which the TMS pulse was applied
    fs:float
        the sampling rate of the signal
    mep_window_in_ms: Tuple[float, float]
        the search window after TMS to look for an iMEP.

    returns
    -------
    amplitude:float
        the  iMEP area


    .. admonition:: Reference

        Rotenberg, A.; Muller, P. A.; Vahabzadeh-Hagh, A. M.; Navarro, X.; López-Vales, R.; Pascual-Leone, A. & Jensen, F. Lateralization of forelimb motor evoked potentials by transcranial magnetic stimulation in rats Clinical Neurophysiology, Elsevier BV, 2010, 121, 104-108

    """
    a = tms_sampleidx + ceil(mep_window_in_ms[0] * fs / 1000)
    # b should not be higher then the len of the trace
    b = ceil(min((tms_sampleidx + (mep_window_in_ms[1] * fs / 1000)), len(trace)))
    amp = np.sum(trace[a:b])
    return amp
