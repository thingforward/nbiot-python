Examples
========

First Steps
-----------
First you should try to connect to your board and auto-attach to the NB network.
If this step succeeds, continue below.

Auto Connect
^^^^^^^^^^^^
If you use a supported board, the lib will auto-detect it:

.. code-block:: python

    import narrowband

    nb = narrowband.Narrowband()
    nb.attach()
    while 1:
        time.sleep(1)

Manual Connect
^^^^^^^^^^^^^^
For any other, defined the device and it's values (port, baudrate and timeout):

.. code-block:: python

    import narrowband

    nb = narrowband.Narrowband("COM1", 9600, 1)
    nb.attach()
    while 1:
        time.sleep(1)


Further Steps
-------------

Send UDP Data
^^^^^^^^^^^^^
todo...
