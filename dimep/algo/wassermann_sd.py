import numpy as np
from numpy import ndarray
from typing import Tuple
from math import ceil
from dimep.tools import bw_boundaries


def wassermann_sd(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 50),
    fs: float = 1000,
    minimum_duration_in_ms: float = 5,
):

    """
    Ziemann, Ulf, Kenji Ishii, Alessandra Borgheresi, Zaneb Yaseen, Fortunato Battaglia, Mark Hallett, Massimo Cincotta, and Eric M. Wassermann. “Dissociation of the Pathways Mediating Ipsilateral and Contralateral Motor-Evoked Potentials in Human Hand and Arm Muscles.” The Journal of Physiology 518, no. 3 (August 1999): 895–906. https://doi.org/10.1111/j.1469-7793.1999.0895p.x.

    "For quantitative analysis of the ipsilateral MEP, single-trial rectification and averaging of the EMG from 20 trials was performed. The level of prestimulus EMG was integrated over a period of 50 ms immediately prior to the magnetic stimulus. The presence of an ipsilateral MEP was accepted if the poststimulus EMG exceeded the prestimulus EMG by at least 1 standard deviation (s.d. ) for at least 5 ms. This EMG peak (dEMG, im µV ms) was expressed as:

    dEMG = (ipsilateral MEP − prestimulus EMG) x  duration of ipsilateral MEP

    where duration is the length of the period during which the poststimulus EMG exceeded the prestimulus EMG. The onset latency of the ipsilateral MEP was defined as the left border of this period. [...] Some target muscles showed no ipsilateral MEPs but rather inhibition of the EMG at the expected time of the ipsilateral MEPs. This inhibition was quantified in a similar way as above."

    """
    minlatency = ceil(mep_window_in_ms[0] * fs / 1000)
    maxlatency = ceil(mep_window_in_ms[1] * fs / 1000)
    baseline_start = tms_sampleidx - ceil(50 * fs / 1000)
    # select baseline and response
    baseline = np.abs(trace)[baseline_start:tms_sampleidx]
    response = np.abs(trace)[tms_sampleidx + minlatency : tms_sampleidx + maxlatency]
    # calculate threshold
    bl_m = baseline.mean()
    bl_s = baseline.std(ddof=1)  # to be consistent with Matlab defaults
    threshold = bl_m + 1 * bl_s

    # select a period of at least 5ms duration

    L = bw_boundaries(response > threshold)
    n = max(L)
    duration = 0
    onset = None
    nix = 1
    while nix <= n:
        tmp = sum(L == nix)
        if tmp > duration:
            duration = tmp
            onset = np.where(L == nix)  # onset = find(L==nix,1);
        nix += 1

    # initialise dEMG
    dEMG = 0.0
    if onset != None:
        duration_in_ms = duration * 1000 / fs
        if duration_in_ms >= minimum_duration_in_ms:
            vpp = np.ptp(response)
            dvpp = vpp - np.ptp(baseline)
            # can be negative, therefore we only use positive values
            dvpp = max([dvpp, 0])
            dEMG = dvpp * duration_in_ms

    return dEMG
