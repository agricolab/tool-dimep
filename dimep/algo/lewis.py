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
from numpy import ndarray
from typing import Tuple
from math import ceil
import numpy as np


def lewis(trace: ndarray, tms_sampleidx: int, fs: float = 1000,) -> float:
    """Estimate iMEP onset and offset based on Lewis 

    Returns the Peak-to-Peak amplitude of the iMEP within 10 to 30ms after stimulus, if it is 'discernable' i.e. at least 100µV in amplitude and exceeds 3 SD of the background EMG (the 30 ms prior to stimulus).

    args
    ----
    trace:ndarray
        the onedimensional EMG signal with units in µV
    tms_sampleidx: int
        the sample at which the TMS pulse was applied
    fs:float
        the sampling rate of the signal

    returns
    -------
    iMEP: float
        the peak-to-peak amplitude of the iMEP


    .. admonition:: Reference

        Lewis, G. N. & Perreault, E. J. Side of lesion influences bilateral activation in chronic, post-stroke hemiparesis. Clinical neurophysiology 2007, 118, 2050-2062 

    .. seealso::

        :func:`~.bradnam`, which inherited the window of 10 to 30ms.

    """
    # NOTE: Formula for SD calculation not given in paper
    """background EMG (30 ms prior to stimulus onset)"""

    baseline_start = tms_sampleidx - ceil(30 * fs / 1000)
    baseline = trace[baseline_start:tms_sampleidx]
    bl_m = baseline.mean()
    bl_s = baseline.std(ddof=1)
    threshold = np.max((bl_m + 3 * bl_s, 100))

    mep_window_in_ms: Tuple[float, float] = (10, 30)
    minlatency = ceil(mep_window_in_ms[0] * fs / 1000)
    maxlatency = mep_window_in_ms[1] * fs / 1000
    maxlatency = ceil(min(maxlatency, len(trace) - tms_sampleidx))
    response = trace[tms_sampleidx + minlatency : tms_sampleidx + maxlatency]
    #  exceed 3 standard deviations (SD) of background EMG.
    # a discernable ipsilateral MEP (iMEP; 10–30 ms onset, >100µV)
    if np.max(response) > threshold:
        return np.ptp(response)
    else:
        return 0.0

