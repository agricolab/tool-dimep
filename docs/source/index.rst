.. DiMEP documentation master file, created by
   sphinx-quickstart on Tue Oct  6 10:21:12 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DiMEP's documentation!
=================================

**DiMEP** stands for **D**\etection of **i**\psilateral **M**\otor **E**\voked **P**\otentials and was developed by `Robert Guggenberger <https://www.robert-guggenberger.de>`_ at the Institute of Neuromodulation and Neurotechnology of the `University Hospital Tübingen <https://www.medizin.uni-tuebingen.de/de/das-klinikum/einrichtungen/kliniken/neurochirurgie-und-neurotechnologie/neuromodulation-und-neurotechnologie>`_.


Installation
------------

.. code-block::

   pip install git+https://github.com/translationalneurosurgery/tool-dimep.git

Usage
-----

Access the algorithms with

.. code-block::

   from dimep.api import <algorithm>

and subsequently call them, e.g. with

.. code-block::

   from dimep.api import lewis
   lewis(trace=trace, tms_sampleidx= 500, fs = 1000)
   # where the trace is the single-channel EMG recording
   # tms_sampleidx marks the onset of the TMS pulse
   # and fs is the sampling rate.


.. toctree::
   :maxdepth: 2
   :caption: Implemented algorithms:

   algorithms



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
