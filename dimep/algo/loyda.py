"""

Ipsilateral  silent  period  and  ipsilateral  motor  evoked  potential.EMG responses in control and stimulated trials (30 of each) were recorded, rectified, and averaged separately for each condition with a custom-made MATLAB program (The MathWorks, Natick, MA).The mean and SD of the background EMG were calculated from a 200-ms window before the onset of the TMS stimulation. When an inhibition of the EMG was observed (iSP), three measures were taken:onset (latency), duration, and area (percentage of inhibition). By using data from the stimulated trials, the iSP onset was determined as thetime point when the EMG dropped below the mean + 1SD for at least 10 ms, and the offset of iSP was the time point when the EMG rebounded above the mean + 1SD. The iSP duration was defined asthe time window from the onset to the offset. The iSP area was calculated by integrating the EMG signal within the time window of the iSP on the control and stimulated trials. The percentage ofinhibition was obtained by dividing the area of the stimulated trial bythe corresponding area on the nonstimulated trial and multiplying by 100

                    mean  area  of  stimulated  trial  
 % Inhibition =     ---------------------------------   x 100
                    mean  area  of unstimulated  trial
                    
When a facilitation (i.e., iMEP) was observed, its onset, offset, andarea (percentage of facilitation) were also calculated in a mannersimilar to the iSP analysis described above, but with the signal rising above the mean baseline + 1SD rather than going below. 

"""
import numpy as np
from numpy import ndarray
from typing import Tuple


def loyda(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 75),
    fs: float = 1000,
    minimum_duration_in_ms: float = 2,
    threshold: float = 0.01,
):
    """Estimate the amplitude of an iMEP

    based  on 
    
    Loyda, J.-C.; Nepveu, J.-F.; Deffeyes, J. E.; Elgbeili, G.; Dancause, N. & Barthélemy, D. Interhemispheric interactions between trunk muscle representations of the primary motor cortex. Journal of neurophysiology, 2017, 118, 1488-1500 

    """
    pass
