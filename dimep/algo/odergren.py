"""
To be accepted as SCM-MEP a minimal upward deflection of 0.1 mV from baseline was required. The peak-to-peak amplitude was given of the SCM-MEP, and the amplitude at the maximal stimulation intensity of each series was determined. The latency of the SCM-MEP was measured from the onset of the sweep triggered by the magnetic stimulation to the onset of upward deflection. 
"""

import numpy as np
from numpy import ndarray
from typing import Tuple


def odergren(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 75),
    fs: float = 1000,
    minimum_duration_in_ms: float = 2,
    threshold: float = 0.01,
):
    """Estimate the amplitude of an iMEP

    based  on 
    
    Odergren, T. & Rimpiläinen, I. Activation and suppression of the sternocleidomastoid muscle induced by transcranial magnetic stimulation 
    Electroencephalography and Clinical Neurophysiology/Electromyography and Motor Control, Elsevier BV, 1996, 101, 175-180

    """
    pass
