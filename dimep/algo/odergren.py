"""
To be accepted as SCM-MEP a minimal upward deflection of 0.1 mV from baseline was required. The peak-to-peak amplitude was given of the SCM-MEP, and the amplitude at the maximal stimulation intensity of each series was determined. The latency of the SCM-MEP was measured from the onset of the sweep triggered by the magnetic stimulation to the onset of upward deflection. 
"""

import numpy as np
from numpy import ndarray, inf
from typing import Tuple
from math import ceil


def odergren(
    trace: ndarray,
    tms_sampleidx: int,
    fs: float = 1000,
    threshold: float = 0.01,
    mep_window_in_ms: Tuple[float, float] = (0, inf),
):
    """Estimate the amplitude of an iMEP based on Odergren 1996

    Returns the PtP-Amplitude of the unrectified EMG if above 0.1mV (100µV) else 0

    .. warning:

        As thresholding is based on absolute values with units, make sure that the units of the trace are in microVolts (µV).

    args
    ----
    trace:ndarray
        the onedimensional EMG signal in units of µV
    tms_sampleidx: int
        the sample at which the TMS pulse was applied
    fs:float
        the sampling rate of the signal
    threshold:float
        the threshold for the iMEP to pass. Defaults to 100 for 100 µV (0.1mV)
    mep_window_in_ms: Tuple[float, float]
        the search window after TMS to look for an iMEP. The manuscript did not specify a restricted search window, and by default we search the whole trace, starting from the TMS to the end of the supplied samples.

    returns
    -------
    amplitude:float
        the peak-to-peak iMEP amplitude of the unrectified EMG after TMS


    .. admonition:: Reference
    
        Odergren, T. & Rimpiläinen, I. Activation and suppression of the sternocleidomastoid muscle induced by transcranial magnetic stimulation Electroencephalography and Clinical Neurophysiology/Electromyography and Motor Control, Elsevier BV, 1996, 101, 175-180

    .. seealso::

        :func:`~.bawa` also takes the PtP amplitude, but does not threshold it

    """
    a = tms_sampleidx + ceil(mep_window_in_ms[0] * fs / 1000)
    # b should not be higher then the len of the trace
    b = ceil(
        min((tms_sampleidx + (mep_window_in_ms[1] * fs / 1000)), len(trace))
    )
    amp = np.ptp(trace[a:b])
    return amp if amp > threshold else 0.0
