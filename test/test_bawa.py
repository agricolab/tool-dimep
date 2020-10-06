from dimep.detect import bawa


def test_bawa(traces):
    for trace in traces:
        bawa(trace, tms_sampleidx=1000)
