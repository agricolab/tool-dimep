"""

To objectively quantify significant ipsilateral responses, 20 TMS stimulations of nonlesioned M1 at 120% RMT were examined for ipsilateral MEP. Participants with ≥5/20 ipsilateral MEP >50 μV in amplitude  were  classified  as  ipsilateral  (IP)  while  those without were considered nonipsilateral (NI). Latencies were calculated as the aver-age time from the TMS artifact (t = 0 ms) to MEP onset  at  120%  RMT.  MEPs  were  recorded  at  rest. Average MEP latency was calculated from 20 MEPs at  120%  RMT.  A  MATLAB  script  identified  MEP  onset as the time point when the EMG exceeded 3 standard deviations from mean background EMG

"""
import numpy as np
from numpy import ndarray
from typing import Tuple


def zewdie(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 75),
    fs: float = 1000,
    minimum_duration_in_ms: float = 2,
    threshold: float = 0.01,
):
    """Estimate the amplitude of an iMEP

    based  on 
    
    Zewdie, E.; Damji, O.; Ciechanski, P.; Seeger, T. & Kirton, A.
    Contralesional Corticomotor Neurophysiology in Hemiparetic Children With Perinatal Stroke. Neurorehabilitation and neural repair, 2017, 31, 261-271 

    """
    pass
