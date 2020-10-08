"""
Because  iMEP  and  iSP  were  generally  of  smallamplitude  and  were  variable  from  trial  to  trial,  we  used  automatedstatistical methods to define their presence. The criteria chosen werebased  on  our  preliminary  studies  to  distinguish  the  changes  frombackground noise. An example of the measurements is shown in Fig.2. For each subject, the surface EMG from the right FDI muscle foreach stimulus intensity and coil orientation were rectified and aver-aged. The mean and SD of the baseline EMG level for 100 ms beforeTMS  was  determined.  An  iMEP  was  deemed  to  be  present  if  thepoststimulus EMG exceeded the prestimulus mean by1SDfor5ms (25 consecutive data points based on 5-kHz sampling rate). iMEPonset  was  defined  as  last  crossing  of  the  mean  baseline  EMG  levelbefore  the  iMEP  peak  and  iMEP  offset  as  thefirst  crossing  of  themean  baseline  EMG  level  after  the  iMEP  peak.  iMEP  area  wascalculated  between  the  iMEP  onset  and  offset.  Similarly,  iSP  wasdeemed significant if the poststimulus EMG fell below the prestimulus mean by1SDfor5 ms (25 consecutive data points based on5-kHz sampling rate). The iSP onset, offset, duration, and area werecalculated similar to that for the iMEP. In some subjects, the iSP wasinterrupted  by“rebound”potential  (Fig.  2)  and  the  iSP  onset  andoffset boundaries included all significant iSP areas. The iSP durationwas  the  time  between  the  onset  and  offset  values.  iMEP  and  iSPthresholds were the lowest stimulus intensities for which we found asignificant response

"""
from numpy import ndarray
from typing import Tuple


def chen(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 75),
    fs: float = 1000,
    minimum_duration_in_ms: float = 2,
    threshold: float = 0.01,
):
    """Estimate the amplitude of an iMEP

    based  on 
    
    Chen, R.; Yung, D. & Li, J.-Y.Organization of Ipsilateral Excitatory and Inhibitory Pathways in the Human Motor Cortex Journal of Neurophysiology, American Physiological Society, 2003, 89, 1256-1264

    """
    pass
