"""
Ziemann, Ulf, Kenji Ishii, Alessandra Borgheresi, Zaneb Yaseen, Fortunato Battaglia, Mark Hallett, Massimo Cincotta, and Eric M. Wassermann. “Dissociation of the Pathways Mediating Ipsilateral and Contralateral Motor-Evoked Potentials in Human Hand and Arm Muscles.” The Journal of Physiology 518, no. 3 (August 1999): 895–906. https://doi.org/10.1111/j.1469-7793.1999.0895p.x.

"For quantitative analysis of the ipsilateral MEP, single-trial rectification and averaging of the EMG from 20 trials was performed. The level of prestimulus EMG was integrated over a period of 50 ms immediately prior to the magnetic stimulus. The presence of an ipsilateral MEP was accepted if the poststimulus EMG exceeded the prestimulus EMG by at least 1 standard deviation (s.d. ) for at least 5 ms. This EMG peak (dEMG, im µV ms) was expressed as:

dEMG = (ipsilateral MEP − prestimulus EMG) x  duration of ipsilateral MEP

where duration is the length of the period during which the poststimulus EMG exceeded the prestimulus EMG. The onset latency of the ipsilateral MEP was defined as the left border of this period. [...] Some target muscles showed no ipsilateral MEPs but rather inhibition of the EMG at the expected time of the ipsilateral MEPs. This inhibition was quantified in a similar way as above."
"""

import numpy as np
from numpy import ndarray
from typing import Tuple
from math import ceil
from dimep.tools import bw_boundaries


def ziemann(
    trace: ndarray,
    tms_sampleidx: int,
    fs: float = 1000,
    minimum_duration_in_ms: float = 5,
) -> float:
    """Estimate the normalized area of of an iMEP based on Ziemann 1999
    
    Returns the normalized area, if it is 1 SD above baseline activity for at least 5ms.

    args
    ----
    trace:ndarray
        the one-dimensional (samples,) EMG signal with units in µV

    tms_sampleidx: int
        the sample at which the TMS pulse was applied

    fs:float
        the sampling rate of the signal

    minimum_duration_in_ms: float = 5
        the number of milliseconds the iMEP needs to be above threshold 

    returns
    -------
    area: float
        the normalized area of the iMEP


    .. admonition:: Reference

        Ziemann, Ulf, Kenji Ishii, Alessandra Borgheresi, Zaneb Yaseen, Fortunato Battaglia, Mark Hallett, Massimo Cincotta, and Eric M. Wassermann. “Dissociation of the Pathways Mediating Ipsilateral and Contralateral Motor-Evoked Potentials in Human Hand and Arm Muscles.” The Journal of Physiology 518, no. 3 (August 1999): 895–906. https://doi.org/10.1111/j.1469-7793.1999.0895p.x.

    .. seealso::

        :func:`~.summers` and :func:`~.bradnam` normalize the iMEP area based on baseline EMG activity. :func:`~.summers` uses higher thresholds, while :func:`~.bradnam` uses similar thresholds, a narrow search window, and calculates the normalization to baseline slightly different.


    """
    baseline_start = tms_sampleidx - ceil(50 * fs / 1000)
    # select baseline and response
    baseline = np.abs(trace)[baseline_start:tms_sampleidx]
    response = np.abs(trace)[tms_sampleidx:]
    # calculate threshold
    bl_m = baseline.mean()
    bl_s = baseline.std(ddof=1)  # to be consistent with Matlab defaults
    threshold = bl_m + 1 * bl_s

    # select a period of at least 5ms duration

    L = bw_boundaries(response > threshold)
    n = max(L)
    active_idx = None
    duration_in_ms: float = 0.0
    nix = 1
    while nix <= n:
        # translate number of samples into duration in ms
        duration_in_ms = sum(L == nix) * 1000 / fs
        if duration_in_ms >= minimum_duration_in_ms:
            active_idx = np.where(L == nix)
            break
        nix += 1

    # active_idx is None if trace is never above threshold for at least 5ms
    if active_idx == None:
        return 0.0
    else:
        # initialise dEMG
        delta: float = float(np.mean(response[active_idx]) - np.mean(baseline))
        # can be negative, therefore we set a boundary at zero (instead
        # of using an if-clause to return 0.0
        delta = max([delta, 0.0])
        dEMG: float = delta * duration_in_ms
        return dEMG
