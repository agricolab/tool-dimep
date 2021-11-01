More Examples
-------------

List available algorithms
+++++++++++++++++++++++++

.. code-block::

   from dimep.api import available
   available()

Mock a trace
++++++++++++

.. code-block::

   # mock a single-channel EMG signal
   from numpy import random
   random.seed(0)
   trace = random.randn(1000)
   print(trace.shape)
   # >>> (1000,)

and subsequently call one (or all) of the algorithms on this mock trace, where the trace is the single-channel EMG recording, tms_sampleidx marks the onset of the TMS pulse and fs is the sampling rate. 

Call all implemented algorithms at once
+++++++++++++++++++++++++++++++++++++++

.. code-block::

   from dimep.api import all
   all(trace, tms_sampleidx=500)
   # >>> {'chen': 0.0,
   #       'bawa': 5.805498168821509,
   #       'bradnam': 0.0,
   #       'guggenberger': 0.11904591308664515,
   #       'lewis': 0.0,
   #       'loyda': 0.0,
   #       'odergren': 0.0,
   #       'rotenberg': 26.662225635355707,
   #       'summers': 0.349919002236347,
   #       'wassermann': 0.7782071535040253,
   #       'zewdie': 0.0,
   #       'ziemann': 0.0}





Access a specific algorithm
+++++++++++++++++++++++++++

.. code-block::

   from dimep.api import <algorithm>


Call a specific algorithm
+++++++++++++++++++++++++

   
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
   