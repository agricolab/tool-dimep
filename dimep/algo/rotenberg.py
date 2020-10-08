"""
To eliminate aver-aging of positive and negative voltages of polyphasic signals, allMEP voltages were converted to absolute values and integratedfor measures of power (area under the curve). [...] Peak-to-peak amplitude, motor thresh-old (MT) and integrated amplitude were computed automaticallyin the 5–30 msec time window, as our pilot data indicated a 4 msecmaximal duration of TMS artifact, and approximately 25 msecmaximal latency to onset of the MEP in rats
"""
import numpy as np
from numpy import ndarray
from typing import Tuple
from math import ceil


def rotenberg(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 50),
    fs: float = 1000,
):
    """Estimate the amplitude of an iMEP

    based on

    Rotenberg, A.; Muller, P. A.; Vahabzadeh-Hagh, A. M.; Navarro, X.; López-Vales, R.; Pascual-Leone, A. & Jensen, F. Lateralization of forelimb motor evoked potentials by transcranial magnetic stimulation in rats Clinical Neurophysiology, Elsevier BV, 2010, 121, 104-108

    """
    a = tms_sampleidx + ceil(mep_window_in_ms[0] * fs / 1000)
    b = tms_sampleidx + ceil(mep_window_in_ms[1] * fs / 1000)
    if np.ndim(trace) == 1:
        return np.ptp(trace[a:b], 0)
    else:
        raise ValueError("Unclear dimensionality of the trace ndarray")
