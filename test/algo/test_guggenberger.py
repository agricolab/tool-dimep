import numpy as np
from dimep.api import guggenberger
from dimep.algo.guggenberger import get_template


def test_guggenberger():
    # assert that the correlation of the template with itself is 1
    assert np.isclose(guggenberger(get_template(fs=1000), 0, 1000), 1)


def test_get_template():
    # morphogenic test independent from the actual length of the template
    f1000 = get_template(fs=1000).shape
    f500 = get_template(fs=500).shape
    assert f1000[0] // 2 == f500[0]
    assert len(f1000) == 1
    assert len(f500) == 1
