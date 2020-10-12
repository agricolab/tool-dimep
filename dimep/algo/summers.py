""" 
Summers, R. L.; Chen, M.; MacKinnon, C. D. & Kimberley, T. J.
Evidence for normal intracortical inhibitory recruitment properties in cervical dystonia  Clinical Neurophysiology, Elsevier BV, 2020, 131, 1272-1279

cSP and iSP data were rectified and a 10 ms moving standard deviation
(SD) calculation was constructed to visualize the waveform. The
average pre-stimulus SD (from -100 ms to -5ms) was used to
construct a threshold to determine the offset of each silent period
according to previously established methods (Chen et al., 2015).
cSP offset was defined as the point that the moving 10 ms SD value
returned to the mean pre-stimulus level. Duration of cSP and iSP
was calculated from the time point of TMS artifact to cSP or iSP off-
set. MEP traces were rectified and averaged for all trials at each
intensity. An iSP was not consistently present across participants
at stimulation intensities <140% cSP threshold, thus the average
iSP waveform for each participant was derived from a minimum
of 5 trials where an iSP was clearly observable at 140% of cSP
threshold. The MEP onset and offset latency was manually deter-
mined from a rectified mean EMG trace constructed from ten trials
using 140% of the silent period threshold. MEP onset and offset
were set at each prominent EMG trace deflection rising or falling
outside of a three SD threshold, constructed from baseline EMG
activity. MEP size was then calculated from each individual trace
using this onset and offset point with the following equation:

MEP size = MEP area - baseline EMG area

where MEP area is the area under the MEP curve and EMG area is the area under the curve for a time-equivalent period of pre-stimulus activity (Bradnam
et al., 2010). """

import numpy as np
from numpy import ndarray, inf
from typing import Tuple
from math import ceil
from dimep.tools import bw_boundaries


def summers_onoff(
    trace: ndarray, tms_sampleidx: int, fs: float = 1000,
) -> Tuple[int, int]:
    """Estimate iMEP onset and offset based on Summers 2020
    
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
    onoff:Tuple[int, int]
        the iMEP onset and offset

    """
    # For each subject, the surface EMG from the right FDI muscle for each
    # stimulus intensity and coil orientation were rectified and averaged.
    rect = np.abs(trace)

    # The average pre-stimulus SD (from -100 ms to -5ms) was used to construct
    # a threshold to determine the offset
    # NOTE: Formula for SD calculation not given in paper
    baseline_start = tms_sampleidx - ceil(100 * fs / 1000)
    baseline_end = tms_sampleidx - ceil(5 * fs / 1000)
    baseline = rect[baseline_start:baseline_end]
    bl_m = baseline.mean()
    bl_s = baseline.std(ddof=1)
    threshold = bl_m + 3 * bl_s

    # MEP onset and offset were set at each prominent EMG trace deflection
    # rising or falling outside of a three SD threshold, constructed from
    # baseline EMG activity.
    response = rect[tms_sampleidx:]
    if not np.any(response > threshold):
        return 0, 0
    L = bw_boundaries(response > threshold)
    n = max(L)
    onset = None
    for nix in range(1, n + 1):
        onset = np.where(L == nix)[0][0]
        break
    if onset is not None:
        try:
            offset = np.where(response[onset:] < threshold)[0][0]
        except IndexError:
            # occurs if response never decreases again below threshold
            offset = len(response)
        onset = onset + tms_sampleidx
        offset = onset + offset
        return onset, offset
    else:
        return 0, 0


def summers(trace: ndarray, tms_sampleidx: int, fs: float = 1000,) -> float:
    """Estimate the area of an iMEP based on Summers 2020

    Normalizes the area by an area of identical duration during baseline, with onset and offset detected by passing a 3SD threshold compared to baseline.

    args
    ----
    trace:ndarray
        the EMG signal

    tms_sampleidx: int
        the sample at which the TMS pulse was applied

    fs:float
        the sampling rate of the signal

    returns
    -------
    amplitude:float
        the iMEPArea based on the rectified EMG normalized by an area of identical duration during baseline


    .. admonition:: Reference
    
        Summers, R. L.; Chen, M.; MacKinnon, C. D. & Kimberley, T. J. Evidence for normal intracortical inhibitory recruitment properties in cervical dystonia  Clinical Neurophysiology, Elsevier BV, 2020, 131, 1272-1279


    .. seealso::

        refers to :func:`~.chen` for using a SD-based threshold amd :func:`~.bradnam` for using a normalization with prestimulus activity. Different to these, a different window for calculation of the baseline mean and SD and a higher threshold is being used. Also, units of the output are differents.

    """

    onset, offset = summers_onoff(
        trace=trace, tms_sampleidx=tms_sampleidx, fs=fs,
    )
    if onset == offset:
        return 0.0
    response = np.abs(trace)
    iMEPArea = np.sum(response[onset:offset])

    # MEP size = MEP area - baseline EMG area
    # where MEP area is the area under the MEP curve and EMG area is the area
    # under the curve for a time-equivalent period of pre-stimulus activity
    # (Bradnam et al., 2010)
    # NOTE: considering Bradnam is specifically cited here, it seems safe to assume that a same buffer of 0.1 ms before the stimulus should be used. Yet, the baseline period is defined as starting at least 5ms before the TMS. Therefore, we implement this using a minimal distance of 5ms
    before = tms_sampleidx - ceil(5 * fs / 1000)  # transform in samples
    duration = offset - onset
    EMGArea = np.sum(response[before - duration : before])

    # calculation as mere difference, not transformed into (µ)V x s but (µ)V x sample
    MEPsize = iMEPArea - EMGArea
    return MEPsize

