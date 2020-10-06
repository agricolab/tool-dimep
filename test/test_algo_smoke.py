from dimep.algo import *
from dimep.algo import __all__
import pytest


@pytest.mark.parametrize("algo", (__all__))
def test_bawa(traces, algo):
    for trace in traces:
        globals()[algo](trace, tms_sampleidx=1000)
