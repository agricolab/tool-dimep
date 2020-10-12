from pytest import fixture
import numpy as np
from pathlib import Path


@fixture(scope="session")
def traces():
    traces = np.load(Path(__file__).parent / "examples.npy")
    yield traces


@fixture(scope="function")
def normtrace():
    trace = np.random.random(2000)  # type: ignore
    s = np.std(trace[0:1000], ddof=1)
    m = np.mean(trace[0:1000])
    trace[0:1000] = (trace[0:1000] - m) / s
    # assert np.std(trace[0:1000], ddof=1) == 1
    s = np.std(trace[1000:], ddof=1)
    m = np.mean(trace[1000:])
    trace[1000:] = (trace[1000:] - m) / s
    # assert np.std(trace[1000:], ddof=1) == 1
    yield trace
