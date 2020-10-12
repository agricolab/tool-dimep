"""

To objectively quantify significant ipsilateral responses, 20 TMS stimulations of nonlesioned M1 at 120% RMT were examined for ipsilateral MEP. Participants with ≥5/20 ipsilateral MEP >50 μV in amplitude  were  classified  as  ipsilateral  (IP)  while  those without were considered nonipsilateral (NI). Latencies were calculated as the aver-age time from the TMS artifact (t = 0 ms) to MEP onset  at  120%  RMT.  MEPs  were  recorded  at  rest. Average MEP latency was calculated from 20 MEPs at  120%  RMT.  A  MATLAB  script  identified  MEP  onset as the time point when the EMG exceeded 3 standard deviations from mean background EMG

A custom MATLAB script calculated
peak-to-peak MEP values from un-rectified EMG by setting
a time window of 15 to 80 ms from the TMS pulse.

"""
import numpy as np
from numpy import ndarray
from typing import Tuple
from math import ceil


def zewdie(
    trace: ndarray,
    tms_sampleidx: int,
    fs: float = 1000,
    discernible_only: bool = False,
) -> float:
    """Estimate the amplitude of an iMEP based on Zewdie 2017


    Returns the Peak-to-Peak amplitude of the iMEP within 15 to 80ms after stimulus, if it is 'discernable' i.e. at least 50µV in amplitude and exceeds 3 SD of the background EMG.

    args
    ----
    trace:ndarray
        the onedimensional EMG signal with units in µV
    tms_sampleidx: int
        the sample at which the TMS pulse was applied
    fs:float
        the sampling rate of the signal
    discernible_only: bool
        whether to report only discernible MEPS (i.e. amplitude >= 50 µV). defaults to False

    returns
    -------
    iMEP: float
        the peak-to-peak amplitude of the iMEP


    .. admonition:: Reference
    
        Zewdie, E.; Damji, O.; Ciechanski, P.; Seeger, T. & Kirton, A.    Contralesional Corticomotor Neurophysiology in Hemiparetic Children With Perinatal Stroke. Neurorehabilitation and neural repair, 2017, 31, 261-271 

    .. seealso::

        :func:`~.odergren` also uses a threshold with absolute units, but 100µV instead of 50µV. :func:`.lewis` is very similar, but uses stricter criterio for discernibility.

    """

    # different to :func:`~.lewis`, the duration of the baseline period is not
    # specified, therefore we include the whole trace until the TMS pulse
    # NOTE: Paper does not specify formula for SD
    baseline = trace[:tms_sampleidx]
    bl_m = baseline.mean()
    bl_s = baseline.std(ddof=1)
    # identified  MEP  onset as the time point when the EMG exceeded 3
    # standard deviations from mean background EMG
    # The paper does not clarify whether this was an additional threshold
    # besides the 50µV, but it seems reasonable
    threshold = bl_m + 3 * bl_s

    mep_window_in_ms: Tuple[float, float] = (15, 80)
    minlatency = ceil(mep_window_in_ms[0] * fs / 1000)
    maxlatency = mep_window_in_ms[1] * fs / 1000
    maxlatency = ceil(min(maxlatency, len(trace) - tms_sampleidx))
    response = trace[tms_sampleidx + minlatency : tms_sampleidx + maxlatency]
    # exceed 3 standard deviations (SD) of background EMG.
    # ipsilateral MEP >50 μV in amplitude
    # NOTE: we take the abs because otherwise, orientiation of the bipolar
    # recording can mess things up
    if np.max(np.abs(response)) > threshold:
        amp = np.ptp(response)
    else:
        amp = 0.0

    if discernible_only:
        return amp if amp >= 50.0 else 0.0
    else:
        return amp
