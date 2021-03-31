import numpy as np
from dimep.api import guggenberger
from dimep.algo.guggenberger import get_template
import pytest


def test_guggenberger():
    # assert that the correlation of the template with itself is 1
    assert np.isclose(guggenberger(get_template(fs=1000), 0, 1000), 1)


def test_guggenberger_amplitude_independence():
    # self-correlation does not depend on the amplitude of the trace
    assert np.isclose(guggenberger(2 * get_template(fs=1000), 0, 1000), 1)


def test_guggenberger_get_template():
    # morphogenic test independent from the actual length of the template
    f1000 = get_template(fs=1000).shape
    f500 = get_template(fs=500).shape
    assert f1000[0] // 2 == f500[0]
    assert len(f1000) == 1
    assert len(f500) == 1


def test_guggenberger_trace_duration():
    # needs to be at least 103ms, i.e. 100ms is not enough
    with pytest.warns(UserWarning):
        guggenberger(np.random.random(200), tms_sampleidx=100, fs=1000)

    # needs to be at least 103ms, e.g. start at 97 to end
    assert guggenberger(np.random.random(200), tms_sampleidx=97, fs=1000)

