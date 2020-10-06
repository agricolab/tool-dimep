import numpy as np
from numpy import ndarray
from typing import Tuple
from math import ceil
from scipy.stats import ttest_1samp


def bawa(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 50),
    fs: float = 1000,
):
    """
    Bawa, P., J.D. Hamm, P. Dhillon, and P.A. Gross. “Bilateral Responses of Upper Limb Muscles to Transcranial Magnetic Stimulation in Human Subjects.” Experimental Brain Research 158, no. 3 (October 2004). https://doi.org/10.1007/s00221-004-2031-x.

    "For each condition and each muscle, unrectified EMG was averaged, and peak-to-peak values of MEPs were measured for the ipsilateral and the contralateral responses"    
    """
    a = tms_sampleidx + ceil(mep_window_in_ms[0] * fs / 1000)
    b = tms_sampleidx + ceil(mep_window_in_ms[1] * fs / 1000)
    if np.ndim(trace) == 1:
        return np.ptp(trace[a:b], 0)
    else:
        raise ValueError("Unclear dimensionality of the trace ndarray")


def wassermann_sd(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 50),
    fs: float = 1000,
    minimum_duration_in_ms: float = 5,
):

    """
    Ziemann, Ulf, Kenji Ishii, Alessandra Borgheresi, Zaneb Yaseen, Fortunato Battaglia, Mark Hallett, Massimo Cincotta, and Eric M. Wassermann. “Dissociation of the Pathways Mediating Ipsilateral and Contralateral Motor-Evoked Potentials in Human Hand and Arm Muscles.” The Journal of Physiology 518, no. 3 (August 1999): 895–906. https://doi.org/10.1111/j.1469-7793.1999.0895p.x.

    "For quantitative analysis of the ipsilateral MEP, single-trial rectification and averaging of the EMG from 20 trials was performed. The level of prestimulus EMG was integrated over a period of 50 ms immediately prior to the magnetic stimulus. The presence of an ipsilateral MEP was accepted if the poststimulus EMG exceeded the prestimulus EMG by at least 1 standard deviation (s.d. ) for at least 5 ms. This EMG peak (dEMG, im µV ms) was expressed as:

    dEMG = (ipsilateral MEP − prestimulus EMG) x  duration of ipsilateral MEP

    where duration is the length of the period during which the poststimulus EMG exceeded the prestimulus EMG. The onset latency of the ipsilateral MEP was defined as the left border of this period. [...] Some target muscles showed no ipsilateral MEPs but rather inhibition of the EMG at the expected time of the ipsilateral MEPs. This inhibition was quantified in a similar way as above."

    """
    minimum_duration = ceil(minimum_duration_in_ms * fs / 1000)
    minlatency = ceil(mep_window_in_ms[0] * fs / 1000)
    maxlatency = ceil(mep_window_in_ms[1] * fs / 1000)
    baseline_start = tms_sampleidx - ceil(50 * fs / 1000)
    # select baseline and response
    baseline = np.abs(trace)[baseline_start:tms_sampleidx]
    response = np.abs(trace)[
        tms_sampleidx + minlatency : tms_sampleidx + maxlatency
    ]
    # calculate threshold
    bl_m = baseline.mean()
    bl_s = baseline.std(ddof=1)  # to be consistent with Matlab defaults
    threshold = bl_m + 1 * bl_s

    # select a period of at least 5ms duration

    L = bw_boundaries(response > threshold)
    n = max(L)
    duration = 0
    onset = None
    nix = 1
    while nix <= n:
        tmp = sum(L == nix)
        if tmp > duration:
            duration = tmp
            onset = np.where(L == nix)  # onset = find(L==nix,1);
        nix += 1

    # initialise dEMG
    dEMG = 0.0
    if onset != None:
        duration_in_ms = duration * 1000 / fs
        if duration_in_ms >= minimum_duration_in_ms:
            vpp = np.ptp(response)
            dvpp = vpp - np.ptp(baseline)
            # can be negative, therefore we only use positive values
            dvpp = max([dvpp, 0])
            dEMG = dvpp * duration_in_ms

    return dEMG


def wassermann_t(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 75),
    fs: float = 1000,
    minimum_duration_in_ms: float = 2,
    threshold: float = 0.01,
):
    """
    Wassermann, Eric M., Alvaro Pascual-Leone, and Mark Hallett. “Cortical Motor Representation of the Ipsilateral Hand and Arm.” Experimental Brain Research 100, no. 1 (July 1994). https://doi.org/10.1007/BF00227284.

    "For statistical testing, the digitized EMG from the ipsilateral target muscle was rectified off line and the trials for each scalp position were averaged. For each position, the averaged data from the 150 ms following the stimulus were divided into 1-ms time bins, and each bin was tested for its difference from the average of all bins in the EMG preceding the stimulus at that position by a t-test. The criterion for significance of an iMEP was the presence of two consecutive 1-ms bins with values above baseline (P < 0.01, 1-tailed t-test) occurring in the 20 ms following the onset of the contralateral MEP evoked at the optimal cMEP position. Positions where significant results were caused by obvious artifacts were excluded from the analysis. The sizes of the iMEP, iSP and late excitatory phases from the FDI were measured for each scalp position in two subjects as follows: First, the baseline EMG value, which was the average of all of the bins preceding the stimulus, was subtracted from all of the bins in each averaged trace. Then the bins corresponding to each of the events (iMEP, iSP, late excitatory phase) in each trace were summed. The boundaries of the epochs containing the events were determined visually by examining the superimposed averaged traces"
    """
    # as the latency of the contralateral MEP might sometimes not be known in
    # general (e.g. after stroke), we let it set as argument and default
    # to expected values from healthy populations
    minlatency = ceil(mep_window_in_ms[0] * fs / 1000)
    maxlatency = ceil(mep_window_in_ms[1] * fs / 1000)
    # there was no information about the baseline period
    #  duration, therefore we
    # used the same period as mentioned in wassermann_sd
    baseline_start = tms_sampleidx - ceil(150 * fs / 1000)
    # select baseline and response
    baseline = np.abs(trace)[baseline_start:tms_sampleidx]
    response = np.abs(trace)[
        tms_sampleidx + minlatency : tms_sampleidx + maxlatency
    ]
    bl_bins = down_bin(baseline, fs / 1000)
    response_bins = down_bin(response, fs / 1000)
    out = ttest_1samp(bl_bins, response_bins)
    # because one-sided
    significant = (out.pvalue < (threshold * 2)) & (out.statistic < 0)

    L = bw_boundaries(significant)
    n = max(L)
    duration = 0
    onset = None
    nix = 1
    while nix <= n:
        tmp = sum(L == nix)
        if tmp > duration:
            duration = tmp
            onset = np.where(L == nix)  # onset = find(L==nix,1);
        nix += 1
    imep = 0
    if onset is not None:
        duration_in_ms = duration * 1000 / fs
        if duration_in_ms >= minimum_duration_in_ms:
            imep = response_bins[onset].mean() - bl_bins.mean()
    return imep


def down_bin(data, binsize: int = 5):
    "downsample an array by binning"
    if binsize == 1:
        return data
    kernel = np.ones(binsize) / binsize
    bins = np.convolve(data, kernel, "same")
    return bins[::binsize]


def bw_boundaries(bools: ndarray) -> ndarray:
    """cluster continous blocks of True in an array
    
    assigns each value in the array a cluster membership number, depending
    on which cluster it belongs.
    
    Example::

        bools = np.asarray((True, False, False, True, True, False), dtype=bool)
        L = bw_boundaries(bools)
        print(L) 
        >>>  [1 0 0 2 2 0]
        
        bools = np.asarray((True, True, False, True, True, False), dtype=bool)
        L = bw_boundaries(bools)
        print(L) 
        >>>  [1 1 0 2 2 0]

    args
    ----
    bools:ndarray
        an array of boolians

    returns
    -------
    L:ndarray
        an array of cluster membership values

    """
    L = np.zeros(bools.shape[0], dtype=np.int)
    i = 0
    counter = 0
    # all values are initially zero, i.e. belong to no cluster
    while i < len(bools) - 1:
        if i == 0 and bools[i] == True:
            # if the starting value is true, this is the first cluster
            # doesn't matter what happened before or after
            counter += 1
            L[i] = counter
            if bools[i + 1] == True:
                L[i + 1] = counter
        elif bools[i] == False and bools[i + 1] == True:
            # if the current value is false, but the next is true,
            # there was a gap. the next value therefore belongs to
            # the next cluster. We therefore increase the cluster counter
            counter += 1
            L[i + 1] = counter
        elif bools[i] == True and bools[i + 1] == True:
            # if the current value is true and the next value is true, the next
            # value belongs to the current cluster. no need to increase the
            # cluster counter
            L[i + 1] = counter
        i += 1
    return L
