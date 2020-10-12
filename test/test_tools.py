from dimep.tools import *
import numpy as np
import pytest


@pytest.mark.parametrize("binsize", np.arange(1.0, 20.0, 1.0))
def test_downbin(binsize):
    x = np.arange(0.0, 100.0, 1)
    if binsize == 1.0:
        xhat = x
    else:
        xhat = np.arange((binsize - 1) / 2, 100.0 - binsize / 2, binsize)

    assert np.allclose(down_bin(x, int(binsize)), xhat)


def test_bwboundaries():
    assert np.allclose(bw_boundaries([0, 1, 1, 0]), [0, 1, 1, 0])
    assert np.allclose(bw_boundaries([0, 1, 1, 0, 1]), [0, 1, 1, 0, 2])
    assert np.allclose(bw_boundaries([1, 1, 1, 0, 1]), [1, 1, 1, 0, 2])
    assert np.allclose(bw_boundaries([1, 1, 1, 1, 1]), [1, 1, 1, 1, 1])
    assert np.allclose(bw_boundaries([1, 1, 0, 0, 1]), [1, 1, 0, 0, 2])
    assert np.allclose(bw_boundaries([1, 1, 0, 1, 0, 1]), [1, 1, 0, 2, 0, 3])
