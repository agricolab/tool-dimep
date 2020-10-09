"""Main Access Point for DiMEP Algorithms"""
from dimep.algo import *
from dimep.version import version


def available() -> None:
    "print all available algorithms"
    from dimep.algo import __all__

    for algo in __all__:
        print(algo)
