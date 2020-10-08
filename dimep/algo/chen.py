"""
Because  iMEP  and  iSP  were  generally  of  small amplitude  and  were  variable  from  trial  to  trial,  we  used  automated statistical methods to define their presence. The criteria chosen werebased  on  our  preliminary  studies  to  distinguish  the  changes  frombackground noise. An example of the measurements is shown in Fig.2. For each subject, the surface EMG from the right FDI muscle for each stimulus intensity and coil orientation were rectified and averaged. The mean and SD of the baseline EMG level for 100 ms before TMS  was  determined.  An  iMEP  was  deemed  to  be  present  if  the poststimulus EMG exceeded the prestimulus mean by >1SD for >= 5ms (25 consecutive data points based on 5-kHz sampling rate). iMEP onset  was  defined  as  last  crossing  of  the  mean  baseline  EMG  level before  the  iMEP  peak  and  iMEP  offset  as  thefirst  crossing  of  themean  baseline  EMG  level  after  the  iMEP  peak.  iMEP  area  wascalculated  between  the  iMEP  onset  and  offset.  Similarly,  iSP  was deemed significant if the poststimulus EMG fell below the prestimulus mean by >=1SD for >5 ms (25 consecutive data points based on5-kHz sampling rate). The iSP onset, offset, duration, and area were calculated similar to that for the iMEP. In some subjects, the iSP was interrupted  by“rebound”potential  (Fig.  2)  and  the  iSP  onset  and offset boundaries included all significant iSP areas. The iSP duration was  the  time  between  the  onset  and  offset  values.  iMEP  and  iSP thresholds were the lowest stimulus intensities for which we found asignificant response

#NOTE for ISP and iMEP, different inequalities are given, but the sample-wise description is identical. 
"""
from numpy import ndarray
from typing import Tuple
from math import ceil
from dimep.tools import bw_boundaries
import numpy as np


def chen(trace: ndarray, tms_sampleidx: int, fs: float = 1000) -> float:
    """Estimate the amplitude of an iMEP

    based  on 
    
    Chen, R.; Yung, D. & Li, J.-Y.Organization of Ipsilateral Excitatory and Inhibitory Pathways in the Human Motor Cortex Journal of Neurophysiology, American Physiological Society, 2003, 89, 1256-1264


    args
    ----
    trace:ndarray
        the recorded EMG signal
    tms_sampleidx: int
        the sample at which the TMS pulse was applied
    fs:float
        the sampling rate of the signal

    """

    # For each subject, the surface EMG from the right FDI muscle for each
    # stimulus intensity and coil orientation were rectified and averaged.
    response = np.abs(trace)

    # The mean and SD of the baseline EMG level for 100 ms before TMS  was
    # determined.
    # NOTE: Formula for SD calculation not given in paper
    baseline_start = tms_sampleidx - ceil(100 * fs / 1000)
    baseline = response[baseline_start:tms_sampleidx]
    bl_m = baseline.mean()
    bl_s = baseline.std(ddof=1)
    threshold = bl_m + 1 * bl_s

    # find the peak, which needs to exceed the prestimulus mean by >1 SD
    L = bw_boundaries(response > threshold)
    n = max(L)
    peak_onset = None
    for nix in range(1, n + 1):
        duration_in_ms = (sum(L == nix) / fs) * 1000
        # for >=5ms
        if duration_in_ms >= 5:
            peak_onset = np.where(L == nix)
            break
    # iMEP onset was defined as last crossing of the mean baseline EMG level
    # before the iMEP peak
    if peak_onset is not None:
        return 0.0
    else:
        onoff = response > bl_m

        """iMEP onset  was  defined  as  last  crossing  of  the  mean  baseline  EMG  level before  the  iMEP  peak """
        # we go backwards in time, starting at the peak_onset
        for ix, v in enumerate(onoff[:peak_onset][::-1]):
            # if the value falls below the treshold of bl_m,
            # it marks the onset
            if v == 0:
                break
        onset = peak_onset - ix

        """iMEP  offset  as  the first  crossing  of  the mean  baseline  EMG  level  after  the  iMEP  peak"""
        # we go forwards in time, starting at the peak_onset
        for ix, v in enumerate(onoff[peak_onset:]):
            # if the value falls below the treshold of bl_m,
            # it marks the offset
            if v == 0:
                break
        offset = peak_onset + ix
        print(onset, offset)

        #  iMEP  area  was calculated  between  the  iMEP  onset  and  offset.
        iMEPArea = np.sum(response[onset:offset])
        return iMEPArea
