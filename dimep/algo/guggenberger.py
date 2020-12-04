import numpy as np
from numpy import ndarray
from scipy.interpolate import interp1d
from scipy.linalg import norm

template = np.atleast_1d(
    [
        0.0025827016085613755,
        -0.008759908769747474,
        0.007249029233268088,
        0.019143168497824686,
        0.02003961200071819,
        0.03184061083773442,
        0.05885472206681661,
        0.09995376794906544,
        0.1657029063878881,
        0.2537555267651536,
        0.3445473264172205,
        0.42773663154415,
        0.4713875473809593,
        0.49213810745828074,
        0.49700403965571366,
        0.46800941385078554,
        0.40825773595992426,
        0.30378416862953633,
        0.1667068550293222,
        0.023846720650167432,
        -0.09303181844210533,
        -0.20261007189238928,
        -0.2878939346417818,
        -0.34018788809441447,
        -0.401031582335873,
        -0.4464401755461463,
        -0.4961852711674143,
        -0.5029959603442864,
        -0.4812863984801352,
        -0.44105287536290483,
        -0.3891440292457928,
        -0.3506554165248879,
        -0.3109021658407735,
        -0.2676302669143019,
        -0.23637110951273385,
        -0.20780914174786064,
        -0.18125804036033344,
        -0.14906661916216035,
        -0.1213815524359073,
        -0.09890424623771082,
        -0.07638588721194779,
        -0.04469596149427363,
        -0.016651034832422307,
        0.012774759901015446,
        0.03104446606243549,
        0.04586474661072469,
        0.06110441121087182,
        0.07296388845602528,
        0.07436432893478861,
        0.0630412011914511,
        0.0632664729975282,
        0.04572642001970844,
        0.036046980160487525,
        0.024723237850641067,
        0.007907311395595449,
        -0.005302529302751823,
        -0.019209134843667944,
        -0.03472377201656734,
        -0.048842733725720844,
        -0.049711783395709384,
        -0.04652200980697414,
        -0.039952965971050795,
        -0.033570339643146846,
        -0.026206220339187614,
        -0.013264898689903876,
        -0.009040103698884173,
        -8.634549881463975e-05,
        0.007844893931203223,
        0.024248214561148732,
        0.0412048111037576,
        0.05411003917403474,
        0.06180799209343158,
        0.07333825579880417,
        0.08283631542955965,
        0.08534277431196542,
        0.09547035436578698,
        0.1045224071286111,
        0.11075868654793278,
        0.10992879543756914,
        0.10988065338898677,
        0.11202113397527731,
        0.11476522681355764,
        0.11056964083053455,
        0.10852479010269993,
        0.09746397206053678,
        0.08071686107364542,
        0.07123046216084931,
        0.06752603243615739,
        0.059543986958047634,
        0.05159736333945624,
        0.05346286127648455,
        0.04952716862105497,
        0.043662944394548674,
        0.03616231128330697,
        0.04354379873272852,
        0.03566566091841854,
        0.03502626791502551,
        0.02538618597195342,
        0.018534783900584315,
        0.009375599579409033,
        0.011524877969209663,
        0.013963787056997922,
        0.0026142903598749163,
    ]
)


def get_template(fs: float) -> ndarray:
    "return the template at the requested sampling rate"
    if fs == 1000.0:
        return template / norm(template)

    x = np.linspace(0, len(template) / 1000, len(template))
    xhat = np.linspace(0, len(template) / 1000, int(len(template) * fs / 1000))
    model = interp1d(x, template)
    itemplate = model(xhat)
    return itemplate / norm(itemplate)


def guggenberger(
    trace: ndarray, tms_sampleidx: int, fs: float = 1000,
) -> float:
    """Estimate amplitude of an iMEP based on Guggenberger (in preparation) 

    Based on the maximal cross-correlation of the signal with the template
    iMEP based on the first component of around 2500 trials


    args
    ----
    trace:ndarray
        the onedimensional EMG signal with units in µV    
        
    tms_sampleidx: int
        the sample at which the TMS pulse was applied

    fs:float
        the sampling rate of the signal
    
    returns
    -------
    iMEP: float
        the maximal cross-correlation score of the iMEP


    .. admonition:: Reference

        Guggenberger et al. (in preparation)
    

    """
    sig = trace[tms_sampleidx:]
    sig = sig / norm(sig)
    xcorr = np.correlate(sig, get_template(fs))
    return np.max(np.abs(xcorr))


def match_template(
    template: ndarray, trace: ndarray, tms_sampleidx: int, fs: float = 1000,
) -> float:
    sig = trace[tms_sampleidx:]
    sig = sig / norm(sig)
    xcorr = np.correlate(sig, template)
    return np.max(np.abs(xcorr))
