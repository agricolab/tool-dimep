import numpy as np
from dimep.api import guggenberger
from dimep.algo.guggenberger import get_template


def test_guggenberger():
    assert np.isclose(guggenberger(get_template(1000), 0, 1000), 1)
