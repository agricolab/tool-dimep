from dimep.algo import *
from dimep.algo import __all__
import pytest


@pytest.mark.parametrize("algo", (__all__))
def test_(traces, algo):
    for trace in traces:
        globals()[algo](trace, tms_sampleidx=1000)


def test_version():
    from dimep.api import version

    assert type(version) == str
