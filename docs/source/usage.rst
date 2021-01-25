More Examples
-------------

List available algorithms
+++++++++++++++++++++++++

.. code-block::

   from dimep.api import available
   available()


Access a specific algorithm
+++++++++++++++++++++++++++

.. code-block::

   from dimep.api import <algorithm>


Call a specific algorithm
+++++++++++++++++++++++++

.. code-block::

   # mock a single-channel EMG signal
   from numpy import random
   random.seed(0)
   trace = random.randn(1000)
   print(trace.shape)
   # >>> (1000,)

and subsequently call one of the algorithms on this mock trace, where the trace is the single-channel EMG recording, tms_sampleidx marks the onset of the TMS pulse and fs is the sampling rate. 
   
For example, the threshold based approach by Lewis (2007)

.. code-block::

   from dimep.api import lewis
   lewis(trace=trace, tms_sampleidx= 500, fs = 1000)
   # >>> 0.0


or the template based approach by Guggenberger (2021):

.. code-block::

   from dimep.api import guggenberger
   guggenberger(trace=trace, tms_sampleidx= 500, fs = 1000)
   # >>> 0.11904591308664515
   