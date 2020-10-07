""" 
Summers, R. L.; Chen, M.; MacKinnon, C. D. & Kimberley, T. J.
Evidence for normal intracortical inhibitory recruitment properties in cervical dystonia  Clinical Neurophysiology, Elsevier BV, 2020, 131, 1272-1279

cSP andiSP data were rectified and a 10 ms moving standard deviation
(SD) calculation was constructed to visualize the waveform. The
average pre-stimulus SD (from 100 ms to 5ms) was used to
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
MEP size 1⁄4 MEP area  baseline EMG area, where MEP area is the
area under the MEP curve and EMG area is the area under the curve
for a time-equivalent period of pre-stimulus activity (Bradnam
et al., 2010). """

import numpy as np
from numpy import ndarray
from typing import Tuple


def summers(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 75),
    fs: float = 1000,
    minimum_duration_in_ms: float = 2,
    threshold: float = 0.01,
):
    """Estimate the amplitude of an iMEP

    based  on 
    
    Summers, R. L.; Chen, M.; MacKinnon, C. D. & Kimberley, T. J.
    Evidence for normal intracortical inhibitory recruitment properties in cervical dystonia  Clinical Neurophysiology, Elsevier BV, 2020, 131, 1272-1279

    """
    pass
