"""
Wassermann, Eric M., Alvaro Pascual-Leone, and Mark Hallett. “Cortical Motor Representation of the Ipsilateral Hand and Arm.” Experimental Brain Research 100, no. 1 (July 1994). https://doi.org/10.1007/BF00227284.

"For statistical testing, the digitized EMG from the ipsilateral target muscle was rectified off line and the trials for each scalp position were averaged. For each position, the averaged data from the 150 ms following the stimulus were divided into 1-ms time bins, and each bin was tested for its difference from the average of all bins in the EMG preceding the stimulus at that position by a t-test. The criterion for significance of an iMEP was the presence of two consecutive 1-ms bins with values above baseline (P < 0.01, 1-tailed t-test) occurring in the 20 ms following the onset of the contralateral MEP evoked at the optimal cMEP position. Positions where significant results were caused by obvious artifacts were excluded from the analysis. The sizes of the iMEP, iSP and late excitatory phases from the FDI were measured for each scalp position in two subjects as follows: First, the baseline EMG value, which was the average of all of the bins preceding the stimulus, was subtracted from all of the bins in each averaged trace. Then the bins corresponding to each of the events (iMEP, iSP, late excitatory phase) in each trace were summed. The boundaries of the epochs containing the events were determined visually by examining the superimposed averaged traces"
"""

import numpy as np
from numpy import ndarray
from typing import Tuple
from math import ceil
from scipy.stats import ttest_1samp
from dimep.tools import down_bin, bw_boundaries


def wassermann(
    trace: ndarray,
    tms_sampleidx: int,
    mep_window_in_ms: Tuple[float, float] = (15, 75),
    fs: float = 1000,
    minimum_duration_in_ms: float = 2,
    threshold: float = 0.01,
) -> float:
    """Estimate the normalized density of an iMEP based on Wassermann 1994

    Uses a statistical test to compare the iMEP versus baseline activity. Only if a block of at least 2ms is significant in a one-sided t-test with p<0.01, the iMEP area average is calculated and normalized to an area of identical duration from the baseline.

    args
    ----
    trace:ndarray
        the one-dimensional (samples,) EMG signal
    tms_sampleidx: int
        the sample at which the TMS pulse was applied
    mep_window_in_ms: Tuple[float, float] = (15, 75),
        the paper describes to have used 'the 20 ms following the onset of the contralateral MEP evoked at the optimal cMEP position'. The latency should therefore be set to your empirical results, e.g. if the latency of the cMEP was 19, set mep_window_in_ms to (19, 39). As the range of latencies in healthy and stroke can vary a lot, we used a very large default range.

    fs:float
        the sampling rate of the signal

    minimum_duration_in_ms: float = 2,
        the papers requires the iMEP to be above threshold for at least 2ms.

    threshold: float = 0.01
        the paper describes to have thresholded for `values above baseline (P < 0.01, 1-tailed t-test)`. The one-tailed test is hardcoded, but you can be flexible with your p-value threshold.


    returns
    -------
    amplitude:float
        the iMEPArea based on the rectified EMG normalized by an area of identical duration during baseline



    .. admonition:: Reference

        Wassermann, Eric M., Alvaro Pascual-Leone, and Mark Hallett. “Cortical Motor Representation of the Ipsilateral Hand and Arm.” Experimental Brain Research 100, no. 1 (July 1994). https://doi.org/10.1007/BF00227284.

    """
    # the original implementation uses 'the 20 ms following the onset of the contralateral MEP evoked at the optimal cMEP position'.
    # the latency of the contralateral MEP is usually around 15-50 ms in
    # but might sometimes not be known in  general (e.g. after stroke), we let it set as argument and sh default
    # to expected values from healthy populations
    minlatency = ceil(mep_window_in_ms[0] * fs / 1000)
    maxhardcodedlatency = ceil(150 * fs / 1000)
    maxlatency = ceil(mep_window_in_ms[1] * fs / 1000)
    maxlatency = min(
        (maxlatency, maxhardcodedlatency, len(trace) - tms_sampleidx)
    )
    # there was no information about the baseline period
    #  duration, therefore we
    # used the same period as mentioned in wassermann_sd
    baseline_start = tms_sampleidx - ceil(150 * fs / 1000)
    # select baseline and response
    baseline = np.abs(trace)[baseline_start:tms_sampleidx]
    response = np.abs(trace)[
        tms_sampleidx + minlatency : tms_sampleidx + maxlatency
    ]
    bl_bins = down_bin(baseline, int(fs / 1000))
    response_bins = down_bin(response, int(fs / 1000))
    out = ttest_1samp(bl_bins, response_bins)
    # because one-sided
    significant = (out.pvalue < (threshold * 2)) & (out.statistic < 0)  # type: ignore

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

