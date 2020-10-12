"""
To be accepted as SCM-MEP a minimal upward deflection of 0.1 mV from baseline was required. The peak-to-peak amplitude was given of the SCM-MEP, and the amplitude at the maximal stimulation intensity of each series was determined. The latency of the SCM-MEP was measured from the onset of the sweep triggered by the magnetic stimulation to the onset of upward deflection. 
"""

import numpy as np
from numpy import ndarray, inf
from typing import Tuple
from math import ceil


def odergren(trace: ndarray, tms_sampleidx: int, fs: float = 1000,) -> float:
    """Estimate the peak-to-peak amplitude of an iMEP based on Odergren 1996

    Returns the PtP-Amplitude of the unrectified EMG if above 0.1mV (100µV) 

    The manuscript did not specify a restricted search window, and by default we search the whole trace, starting from the TMS to the end of the supplied samples.

    .. warning:

        As thresholding is also based on absolute values with units, make sure that the units of the trace are in microVolts (µV).

    args
    ----
    trace:ndarray
        the onedimensional EMG signal in units of µV
        
    tms_sampleidx: int
        the sample at which the TMS pulse was applied

    fs:float
        the sampling rate of the signal

    returns
    -------
    amplitude:float
        the peak-to-peak iMEP amplitude of the unrectified EMG after TMS


    .. admonition:: Reference
    
        Odergren, T. & Rimpiläinen, I. Activation and suppression of the sternocleidomastoid muscle induced by transcranial magnetic stimulation Electroencephalography and Clinical Neurophysiology/Electromyography and Motor Control, Elsevier BV, 1996, 101, 175-180

    .. seealso::

        :func:`~.bawa` also takes the PtP amplitude, but does not threshold it

    """
    amp = np.ptp(trace[tms_sampleidx:])
    return amp if amp >= 100 else 0.0
