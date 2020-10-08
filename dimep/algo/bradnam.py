"""
To determine iMEPs from background EMG activity, left INF EMG was rectifiedoff-line using Signal software (CED, Cambridge, UK), then averagedand inspected for iMEPs between 10 and 30 ms poststimulus, similarto published protocols (Chen et al. 2003; Lewis and Perreault 2007).iMEPs were only evoked with stimulation intensities of 80 and 90%MSO, in 8 participants. Onset and offset latencies of the largest leftINF iMEP were determined and used to calculate iMEPAREAfor thatparticipant (11 – 28 ms depending on the individual) (Fig. 2A). To account for any differences in background EMG, EMGAREA was calculated for each trial, in a window of prestimulus EMG equivalentin duration to that of the iMEPAREAanalysis window, ending 0.1 msbefore the stimulus.iMEP size was calculated for each trial, by sub-tracting background EMGAREA from the iMEPAREA using the formula:

iMEP = (iMEPAREA - EMGAREA) x 1,000

where iMEPAREA is the area calculated between iMEP onset and offset latencies, EMGAREA isthe background EMG area calculated over the same duration as the iMEPAREA, converted to mV·s. 
"""
from numpy import ndarray
from typing import Tuple
import numpy as np
from math import ceil


def bradnam(
    trace: ndarray, tms_sampleidx: int, fs: float = 1000,
):
    """Estimate iMEP amplitude based on Bradnam 2010 (fork of Chen 2003)

    Similar to :func:`~.chen`, the iMEP area is calculated from the rectified EMG, if at least 5ms are 1SD above the mean of the baseline. In addition, the value for an area of identical duration during the baseline period immediatly before the TMS is subtracted and multiplied by 1000:

    iMEP = (iMEPAREA - EMGAREA) x 1,000

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
        the normalized iMEP Area based on the rectified EMG     


    .. admonition:: Reference
        
        Bradnam, L. V.; Stinear, C. M.; Lewis, G. N. & Byblow, W. D.Task-Dependent Modulation of Inputs to Proximal Upper Limb Following Transcranial Direct Current Stimulation of Primary Motor Cortex Journal of Neurophysiology, American Physiological Society, 2010, 103, 2382-2389

    .. seealso::

        :py:func:`~.bradnam` is based on  but normalizes the iMEP amplitude by baseline EMG activity

    """
    from dimep.algo.chen import chen_onoff

    # inspected for iMEPs between 10 and 30 ms poststimulus,
    mep_window_in_ms: Tuple[float, float] = (10, 30)
    # For each subject, the surface EMG from the right FDI muscle for each
    # stimulus intensity and coil orientation were rectified and averaged.

    onset, offset = chen_onoff(trace=trace, tms_sampleidx=tms_sampleidx, fs=fs)
    # For each subject, the surface EMG from the right FDI muscle for each
    # stimulus intensity and coil orientation were rectified and averaged.
    response = np.abs(trace)
    iMEPArea = np.sum(response[onset:offset])
    # EMGAREA isthe background EMG area calculated over the same duration as
    # the iMEPAREA
    # EMGAREA was calculated for each trial, in a window of prestimulus EMG
    # equivalent in duration to that of the iMEPAREAanalysis window,
    # ending 0.1 ms before the stimulus.
    before = tms_sampleidx - ceil(0.1 * fs / 1000)  # transform in samples
    duration = offset - onset
    EMGArea = np.sum(response[before - duration : before])
    # return (iMEPArea - EMGArea) * 1000
    """converted to mV·s."""
    # this would be the case if me divivde by fs, not necessaruily 1000:
    # therefore
    return ((iMEPArea - EMGArea) / fs) * 1000

