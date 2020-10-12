"""

Ipsilateral  silent  period  and  ipsilateral  motor  evoked  potential. EMG responses in control and stimulated trials (30 of each) were recorded, rectified, and averaged separately for each condition with a custom-made MATLAB program (The MathWorks, Natick, MA).The mean and SD of the background EMG were calculated from a 200-ms window before the onset of the TMS stimulation. When an inhibition of the EMG was observed (iSP), three measures were taken:onset (latency), duration, and area (percentage of inhibition). By using data from the stimulated trials, the iSP onset was determined as thetime point when the EMG dropped below the mean + 1SD for at least 10 ms, and the offset of iSP was the time point when the EMG rebounded above the mean + 1SD. The iSP duration was defined asthe time window from the onset to the offset. The iSP area was calculated by integrating the EMG signal within the time window of the iSP on the control and stimulated trials. The percentage ofinhibition was obtained by dividing the area of the stimulated trial bythe corresponding area on the nonstimulated trial and multiplying by 100

                    mean  area  of  stimulated  trial  
 % Inhibition =     ---------------------------------   x 100
                    mean  area  of unstimulated  trial
                    
When a facilitation (i.e., iMEP) was observed, its onset, offset, andarea (percentage of facilitation) were also calculated in a mannersimilar to the iSP analysis described above, but with the signal rising above the mean baseline + 1SD rather than going below. 

"""
import numpy as np
from numpy import ndarray
from typing import Tuple, Union
from dimep.tools import bw_boundaries
from math import ceil


def loyda_onoff(
    trace: ndarray,
    tms_sampleidx: int,
    fs: float = 1000,
    mep_window_in_ms: Tuple[float, float] = (0, np.inf),
    baseline_duration_in_ms: float = 200,
    minimum_duration_in_ms: float = 10,
) -> Tuple[int, int]:
    """Estimate iMEP onset and offset based on Loyda 2017

    args
    ----
    trace:ndarray
        the onedimensional EMG signal
    tms_sampleidx: int
        the sample at which the TMS pulse was applied
    fs:float
        the sampling rate of the signal
    mep_window_in_ms: Tuple[float, float]
        the search window after TMS to look for an iMEP
    baseline_duration_in_ms: float
        the duration of the baseline period immediatly before TMS
    minimum_duration_in_ms:float
        the minimum duration above threshold to count as iMEP

    returns
    -------
    onoff:Tuple[int, int]
        the iMEP onset and offset

    """
    # EMG responses [...] were [...] rectifiedd.
    rect = np.abs(trace)

    # select baseline and response

    # The mean and SD of the background EMG were calculated from a 200-ms window before the onset of the TMS stimulation
    # NOTE: Formula for SD calculation not given in paper
    baseline_start = tms_sampleidx - ceil(baseline_duration_in_ms * fs / 1000)
    baseline = rect[baseline_start:tms_sampleidx]
    bl_m = baseline.mean()
    bl_s = baseline.std(ddof=1)
    threshold = bl_m + 1 * bl_s

    # with the signal rising above the mean baseline + 1SD rather than going below
    minlatency = ceil(mep_window_in_ms[0] * fs / 1000)
    maxlatency = mep_window_in_ms[1] * fs / 1000
    maxlatency = ceil(min(maxlatency, len(trace) - tms_sampleidx))
    response = rect[tms_sampleidx + minlatency : tms_sampleidx + maxlatency]
    L = bw_boundaries(response > threshold)
    n = max(L)
    onset = None
    for nix in range(1, n + 1):
        duration_in_ms = (sum(L == nix) / fs) * 1000
        #  for at least 10 ms
        if duration_in_ms >= minimum_duration_in_ms:
            onset = np.where(L == nix)[0][0]
            break
    # onset was determined as the time point when the EMG  [rose above]  mean + 1SD for at least 10 ms, and the offset [...] was the time point when the EMG rebounded [below] the mean + 1SD.
    if onset is None:
        return (0, 0)
    else:
        # we go forwards in time, starting at the onset
        ix = 0
        for ix, v in enumerate(response[onset:] > threshold):
            # if the value falls below the treshold, it marks the offset
            if v == 0:
                break

        onset = tms_sampleidx + minlatency + onset
        offset = onset + ix
        return (onset, offset)


def loyda(
    trace: ndarray,
    tms_sampleidx: int,
    fs: float = 1000,
    sham_trace: Union[ndarray, None] = None,
) -> float:
    """Estimate the normalized density of an iMEP based on Loyda 2017

    The iMEP area is calculated from the rectified EMG, if at least 10ms are 1SD above the mean of the baseline of the 200ms before TMS, and additionally normalized by the area of an identical period from a nonstimulation trial. 


    args
    ----
    trace:ndarray
        the EMG signal
        
    tms_sampleidx: int
        the sample at which the TMS pulse was applied

    fs:float
        the sampling rate of the signal

    sham_trace: Union[ndarray, None]
        if not supplied, the function will take a period from before the TMS period to calculate a shamArea for normalization. Otherwise, support a non-stimulation trial for strict estimation following Loyda 2017

    returns
    -------
    amplitude:float
        the iMEP Area based on the rectified EMG     

    .. admonition:: Reference  
    
    Loyda, J.-C.; Nepveu, J.-F.; Deffeyes, J. E.; Elgbeili, G.; Dancause, N. & Barthélemy, D. Interhemispheric interactions between trunk muscle representations of the primary motor cortex. Journal of neurophysiology, 2017, 118, 1488-1500 

    """
    onset, offset = loyda_onoff(trace, tms_sampleidx=tms_sampleidx, fs=fs)
    if onset == offset:
        return 0.0
    iMEPArea = np.mean(np.abs(trace[onset:offset]))

    """The percentage [...] was obtained by dividing the area of the
    stimulated trial by the corresponding area on the nonstimulated trial and
    multiplying by 100"""
    # considering we do not necessarily have unstimulated trials, we try to
    # mimic this
    if sham_trace is None:
        try:
            # we go backwards from the tms. Because onset and offset are sampleindices, we flip the along the tms_sampleidx
            shamArea = np.mean(
                np.abs(
                    trace[
                        2 * tms_sampleidx - offset : 2 * tms_sampleidx - onset
                    ]
                )
            )
        except IndexError:
            raise IndexError(
                "I can not mimic a sham_trace with the baselineperiod, please supply a trace of identical length without stimulation"
            )
    else:
        shamArea = np.mean(np.abs(sham_trace[onset:offset]))

    if shamArea == 0.0:
        raise ValueError(
            "Sham Area is too close to zero for numerical stability"
        )
    return (iMEPArea / shamArea) * 100
