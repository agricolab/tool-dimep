"""
To determine iMEPs from background EMG activity, left INF EMG was rectifiedoff-line using Signal software (CED, Cambridge, UK), then averagedand inspected for iMEPs between 10 and 30 ms poststimulus, similarto published protocols (Chen et al. 2003; Lewis and Perreault 2007).iMEPs were only evoked with stimulation intensities of 80 and 90%MSO, in 8 participants. Onset and offset latencies of the largest leftINF iMEP were determined and used to calculate iMEPAREAfor thatparticipant (11 – 28 ms depending on the individual) (Fig. 2A). To account for any differences in background EMG, EMGAREA was calculated for each trial, in a window of prestimulus EMG equivalentin duration to that of the iMEPAREAanalysis window, ending 0.1 msbefore the stimulus.iMEP size was calculated for each trial, by sub-tracting background EMGAREA from the iMEPAREA using the formula:

iMEP = (iMEPAREA - EMGAREA) x 1,000

where iMEPAREA is the area calculated between iMEP onset and offset latencies, EMGAREA isthe background EMG area calculated over the same duration as the iMEPAREA, converted to mV·s. 
"""
from numpy import ndarray
from typing import Tuple


def bradnam(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 75),
    fs: float = 1000,
    minimum_duration_in_ms: float = 2,
    threshold: float = 0.01,
):
    """Estimate the amplitude of an iMEP

    based  on 
    
    Bradnam, L. V.; Stinear, C. M.; Lewis, G. N. & Byblow, W. D.
    Task-Dependent Modulation of Inputs to Proximal Upper Limb Following Transcranial Direct Current Stimulation of Primary Motor Cortex 
    Journal of Neurophysiology, American Physiological Society, 2010, 103, 2382-2389

    """
    rect = np.abs(trace)
