from numpy import ndarray
import numpy as np
from pathlib import Path
from pkg_resources import get_distribution

root = Path(get_distribution("dimep").location)


def down_bin(data: ndarray, binsize: int = 5):
    "downsample an array by binning"
    if binsize == 1:
        return data
    kernel: ndarray = np.ones(binsize) / binsize
    bins: ndarray = np.convolve(data, kernel, "valid")
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
    bools = np.asarray_chkfinite(bools)
    L: ndarray = np.zeros(bools.shape[0], dtype=np.int)
    i: int = 0
    counter: int = 0
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
