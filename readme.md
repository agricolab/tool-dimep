
[![status](https://github.com/translationalneurosurgery/tool-dimep/workflows/pytest/badge.svg)](https://github.com/translationalneurosurgery/tool-dimep/actions) [![Documentation Status](https://readthedocs.org/projects/tool-dimep/badge/?version=latest)](https://tool-dimep.readthedocs.io/en/latest/?badge=latest) [![Coverage Status](https://coveralls.io/repos/github/translationalneurosurgery/tool-dimep/badge.svg?branch=develop)](https://coveralls.io/github/translationalneurosurgery/tool-dimep?branch=develop) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://en.wikipedia.org/wiki/MIT_License)


# Detection of Ipsilateral Motor Evoked Potentials

**DiMEP** stands for **D**etection of **i**psilateral **M**otor **E**voked **P**otentials and was developed by [Robert Guggenberger](https://www.robert-guggenberger.de) at the [Institute of Neuromodulation and Neurotechnology of the University Hospital Tübingen](https://www.medizin.uni-tuebingen.de/de/das-klinikum/einrichtungen/kliniken/neurochirurgie-und-neurotechnologie/neuromodulation-und-neurotechnologie>).


Installation
------------

``` bash

   pip install git+https://github.com/translationalneurosurgery/tool-dimep.git

```

Usage
-----

Access the algorithms with

``` python

   from dimep.api import <algorithm>

```
and subsequently call them, e.g. with

``` python

   from dimep.api import lewis
   lewis(trace=trace, tms_sampleidx= 500, fs = 1000)
   # where the trace is the single-channel EMG recording
   # tms_sampleidx marks the onset of the TMS pulse
   # and fs is the sampling rate.
```

Documentation
-------------

Read the documentation on [readthedocs](https://readthedocs.org/projects/tool-dimep/badge/?version=latest).