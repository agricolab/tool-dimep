from pytest import fixture
import numpy as np
from pathlib import Path


@fixture(scope="session")
def traces():
    traces = np.load(Path(__file__).parent / "examples.npy")
    yield traces
