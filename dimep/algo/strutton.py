"""
Bilateral EMG responses wererecorded simultaneously from all three muscles and were rectified and then averaged for each trial. The times ofonset and finish of the MEP were determined visually bytwo independent assessors and cursors positioned at thesepoints to allow measurement of latency and area.
"""
import numpy as np
from numpy import ndarray
from typing import Tuple
from math import ceil


def strutton(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 50),
    fs: float = 1000,
):
    """Estimate the amplitude of an iMEP

    based on

    Strutton, P.; Beith, I.; Theodorou, S.; Catley, M.; McGregor, A. & Davey, N. Corticospinal activation of internal oblique muscles has a strong ipsilateral component and can be lateralised in man Experimental Brain Research, Springer Science and Business Media LLC, 2004, 158

    """
    a = tms_sampleidx + ceil(mep_window_in_ms[0] * fs / 1000)
    b = tms_sampleidx + ceil(mep_window_in_ms[1] * fs / 1000)
    if np.ndim(trace) == 1:
        return np.ptp(trace[a:b], 0)
    else:
        raise ValueError("Unclear dimensionality of the trace ndarray")
