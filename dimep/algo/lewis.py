"""

MEP latency and maximum peak-to-peak amplitude values were obtained. MEP
latency was defined as the first point following the stimulus
artifact to exceed 3 standard deviations (SD) of back-
ground EMG. MEP amplitude was determined as the max-
imum peak-to-peak difference in response size in a 30 ms
window following the onset of the response.

Similar analyses were used
to compare the level of background EMG (30 ms prior to
stimulus onset) between the two sets of tasks with matched
muscle activation.

Responses in the muscle ipsilateral to cortical stimula-tion were analyzed in the two tasks in which the ipsilateralmuscle was activated during stimulation (ipsilateral activa-tion, bilateral activation). The number of stimuli that gave rise to a discernable ipsilateral MEP (iMEP; 10–30 ms onset, >100µV) was recorded for all stimulus intensitiesand converted to a percentage of total stimuli given.
"""
from numpy import ndarray, inf
from typing import Tuple
from math import ceil
import numpy as np


def lewis(
    trace: ndarray,
    tms_sampleidx: int,
    fs: float = 1000,
    discernible_only: bool = False,
) -> float:
    """Estimate peak-to-peak amplitude of an iMEP based on Lewis 2007

    Returns the Peak-to-Peak amplitude of the iMEP within 10 to 30ms after stimulus, if it is 'discernable' i.e. at least 100µV in amplitude and exceeds 3 SD of the background EMG (the 30 ms prior to stimulus).

    args
    ----
    trace:ndarray
        the one-dimensional (samples,) EMG signal with units in µV
    tms_sampleidx: int
        the sample at which the TMS pulse was applied
    fs:float
        the sampling rate of the signal
    discernible_only:bool
        whether to report only discernible MEPS (i.e. onset within 10-30ms after TMS and amplitude >= 100 µV). defaults to False

    returns
    -------
    iMEP: float
        the peak-to-peak amplitude of the iMEP


    .. admonition:: Reference

        Lewis, G. N. & Perreault, E. J. Side of lesion influences bilateral activation in chronic, post-stroke hemiparesis. Clinical neurophysiology 2007, 118, 2050-2062 

    .. seealso::

        :func:`~.bradnam`, which inherited the window of 10 to 30ms, or :func:`~.zewdie`, which also calculated PtP, but uses a window from 15 to 80ms and a lower threshold of 50µV.

    """
    # NOTE: Formula for SD calculation not given in paper
    """background EMG (30 ms prior to stimulus onset)"""

    baseline_start = tms_sampleidx - ceil(30 * fs / 1000)
    baseline = trace[baseline_start:tms_sampleidx]
    bl_m = baseline.mean()
    bl_s = baseline.std(ddof=1)
    sd_threshold = bl_m + 3 * bl_s

    response = trace[tms_sampleidx:]  # recording after TMS
    mep_window_in_ms: Tuple[float, float]
    if discernible_only:
        mep_window_in_ms = (10.0, 30.0)
    else:
        mep_window_in_ms = (0.0, inf)

    minlatency = ceil(mep_window_in_ms[0] * fs / 1000)
    maxlatency = mep_window_in_ms[1] * fs / 1000
    maxlatency = ceil(min(maxlatency, len(trace) - tms_sampleidx))
    #  latency was defined as the first point following the stimulus
    # artifact to exceed 3 standard deviations (SD) of background EMG
    # a discernable ipsilateral MEP (iMEP; 10–30 ms onset, >100µV)
    onset = (
        np.where(np.abs(response[minlatency:maxlatency]) >= sd_threshold)[0]
        + minlatency
    )
    if len(onset) > 0:
        onset = onset[0]
        # MEP amplitude was determined as the maximum peak-to-peak difference
        # in response size in a 30 ms window following the onset of the
        # response.
        window = onset + ceil(30 * fs / 1000)
        amp = np.ptp(response[onset : onset + window])
    else:
        amp = 0.0
    if discernible_only:
        return amp if amp >= 100.0 else 0.0
    else:
        return amp

