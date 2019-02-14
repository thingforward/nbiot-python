==============
Narrowband API
==============

NarrowBand
----------
.. class:: NarrowBand

    .. method:: set_cdp(hostname)
	    :param hostname: 
		    Your CDP hostname
			
	Disables the module functionality, sets your CDP and re-enables it.
			
    .. method:: set_apn(apn)
	    :param apn:
		    Your APN hostname
			
	Sets your APN.
			
	.. method:: attach()
	
    Enables and tracks the signalling connection, network registration and attachment status.
    Loops and waits until connection to NB-IoT network succeeds. 	
	    
NarrowBandCore
--------------
.. class:: NarrowBandCore

    coming soon...