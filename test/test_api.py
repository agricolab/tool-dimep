from dimep.api import *
from dimep.tools import root


def test_available(capsys):
    out = capsys.readouterr
    available()
    out = capsys.readouterr()
    for algo in (root / "dimep" / "algo").glob("*.py"):
        if algo.stem[0] != "_":
            assert algo.stem in out.out
