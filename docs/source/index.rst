.. DiMEP documentation master file, created by
   sphinx-quickstart on Tue Oct  6 10:21:12 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DiMEP's documentation!
=================================

**DiMEP** stands for **D**\etection of **i**\psilateral **M**\otor **E**\voked **P**\otentials and was developed by `Robert Guggenberger <https://www.agricolab.de>`_ at the Institute of Neuromodulation and Neurotechnology of the `University Hospital Tübingen <https://www.medizin.uni-tuebingen.de/de/das-klinikum/einrichtungen/kliniken/neurochirurgie-und-neurotechnologie/neuromodulation-und-neurotechnologie>`_.


Installation
------------

Stable 
++++++

.. code-block::

   pip install dimep


Development
+++++++++++

.. code-block::

   pip install git+https://github.com/translationalneurosurgery/tool-dimep.git


Example
-------

.. code-block::

   # mock a single-channel EMG signal
   from numpy import random
   random.seed(0)
   trace = random.randn(1000)
   print(trace.shape)
   # >>> (1000,)

   # and apply the template approach on this trace   
   # where the trace is the single-channel EMG recording
   # tms_sampleidx marks the onset of the TMS pulse
   # and fs is the sampling rate.
   from dimep.api import guggenberger
   guggenberger(trace=trace, tms_sampleidx= 500, fs = 1000)
   # >>> 0.11904591308664515


Documentation
-------------

.. toctree::
   :maxdepth: 2
   
   usage
   algorithms   
   support


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
