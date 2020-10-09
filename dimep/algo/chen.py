"""
Because  iMEP  and  iSP  were  generally  of  small amplitude  and  were  variable  from  trial  to  trial,  we  used  automated statistical methods to define their presence. The criteria chosen werebased  on  our  preliminary  studies  to  distinguish  the  changes  frombackground noise. An example of the measurements is shown in Fig.2. For each subject, the surface EMG from the right FDI muscle for each stimulus intensity and coil orientation were rectified and averaged. The mean and SD of the baseline EMG level for 100 ms before TMS  was  determined.  An  iMEP  was  deemed  to  be  present  if  the poststimulus EMG exceeded the prestimulus mean by >1SD for >= 5ms (25 consecutive data points based on 5-kHz sampling rate). iMEP onset  was  defined  as  last  crossing  of  the  mean  baseline  EMG  level before  the  iMEP  peak  and  iMEP  offset  as  thefirst  crossing  of  themean  baseline  EMG  level  after  the  iMEP  peak.  iMEP  area  wascalculated  between  the  iMEP  onset  and  offset.  Similarly,  iSP  was deemed significant if the poststimulus EMG fell below the prestimulus mean by >=1SD for >5 ms (25 consecutive data points based on5-kHz sampling rate). The iSP onset, offset, duration, and area were calculated similar to that for the iMEP. In some subjects, the iSP was interrupted  by“rebound”potential  (Fig.  2)  and  the  iSP  onset  and offset boundaries included all significant iSP areas. The iSP duration was  the  time  between  the  onset  and  offset  values.  iMEP  and  iSP thresholds were the lowest stimulus intensities for which we found asignificant response

#NOTE for ISP and iMEP, different inequalities are given, but the sample-wise description is identical. 
"""
from numpy import ndarray, inf
from typing import Tuple
from math import ceil
from dimep.tools import bw_boundaries
import numpy as np


def chen_onoff(
    trace: ndarray,
    tms_sampleidx: int,
    fs: float = 1000,
    mep_window_in_ms: Tuple[float, float] = (0, inf),
    baseline_duration_in_ms: float = 100,
) -> Tuple[int, int]:
    """Estimate iMEP onset and offset based on Chen 2003
    
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

    returns
    -------
    onoff:Tuple[int, int]
        the iMEP onset and offset

    """
    # For each subject, the surface EMG from the right FDI muscle for each
    # stimulus intensity and coil orientation were rectified and averaged.
    rect = np.abs(trace)

    # select baseline and response

    # The mean and SD of the baseline EMG level for 100 ms before TMS  was
    # determined.
    # NOTE: Formula for SD calculation not given in paper
    baseline_start = tms_sampleidx - ceil(baseline_duration_in_ms * fs / 1000)
    baseline = rect[baseline_start:tms_sampleidx]
    bl_m = baseline.mean()
    bl_s = baseline.std(ddof=1)
    threshold = bl_m + 1 * bl_s

    # find the peak, which needs to exceed the prestimulus mean by >1 SD
    minlatency = ceil(mep_window_in_ms[0] * fs / 1000)
    maxlatency = mep_window_in_ms[1] * fs / 1000
    maxlatency = ceil(min(maxlatency, len(trace) - tms_sampleidx))
    response = rect[tms_sampleidx + minlatency : tms_sampleidx + maxlatency]
    L = bw_boundaries(response > threshold)
    n = max(L)
    peak_onset = None
    for nix in range(1, n + 1):
        duration_in_ms = (sum(L == nix) / fs) * 1000
        # for >=5ms
        if duration_in_ms >= 5:
            peak_onset = np.where(L == nix)[0][0]
            break
    # iMEP onset was defined as last crossing of the mean baseline EMG level
    # before the iMEP peak
    if peak_onset is None:
        return (0, 0)
    else:
        onoff = response > bl_m

        """iMEP onset  was  defined  as  last  crossing  of  the  mean  baseline  EMG  level before  the  iMEP  peak """
        # we go backwards in time, starting at the peak_onset\
        ix = 0
        for ix, v in enumerate(onoff[:peak_onset][::-1]):
            # if the value falls below the treshold of bl_m,
            # it marks the onset
            if v == 0:
                break
        onset = tms_sampleidx + minlatency + peak_onset - ix

        """iMEP  offset  as  the first  crossing  of  the mean  baseline  EMG  level  after  the  iMEP  peak"""
        # we go forwards in time, starting at the peak_onset
        ix = 0
        for ix, v in enumerate(onoff[peak_onset:]):
            # if the value falls below the treshold of bl_m,
            # it marks the offset
            if v == 0:
                break
        offset = tms_sampleidx + minlatency + peak_onset + ix
        return (onset, offset)


def chen(trace: ndarray, tms_sampleidx: int, fs: float = 1000) -> float:
    """Estimate iMEP amplitude based on Chen 2003

    The iMEP area is calculated from the rectified EMG, if at least 5ms are 1SD above the mean of the baseline. A fork is :func:`~.chen`.


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
        the iMEP Area based on the rectified EMG     


    .. admonition:: Reference
        
        Chen, R.; Yung, D. & Li, J.-Y.Organization of Ipsilateral Excitatory and Inhibitory Pathways in the Human Motor Cortex Journal of Neurophysiology, American Physiological Society, 2003, 89, 1256-1264

    .. seealso::

        :py:func:`~.bradnam` is based on :func:`~.chen` but normalizes the iMEP amplitude by baseline EMG activity

    """
    # We factored the determination of onset and offset out of this function, # because it will also be used for :func:`~.bradnam`
    onset, offset = chen_onoff(trace=trace, tms_sampleidx=tms_sampleidx, fs=fs)

    # For each subject, the surface EMG from the right FDI muscle for each
    # stimulus intensity and coil orientation were rectified and averaged.
    response = np.abs(trace)
    iMEPArea = np.sum(response[onset:offset])
    return iMEPArea
