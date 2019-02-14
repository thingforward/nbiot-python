==============
Narrowband API
==============

NarrowBand
----------
.. class:: NarrowBand

    .. method:: set_cdp(hostname)
	
        :param str hostname: Your CDP hostname
		    
        Disables the module functionality, sets your CDP and re-enables it.
			
    .. method:: set_apn(apn)
	
        :param str apn: Your APN hostname

        Sets your APN.
			
    .. method:: attach()

        Enables and tracks the signalling connection, network registration and attachment status.
        Loops and waits until connection to NB-IoT network succeeds. 

    .. method:: send_udp(remote_addr, remote_port, data)

        :param str remote_addr: Remote address to receive data at
        :param str remote_port: Remote port to receive data at
        :param str data: Data to send

        Auto-converts the string data to a proper ByteArray and sends it via UDP to the given IP address.
	    
NarrowBandCore
--------------
.. class:: NarrowBandCore

    coming soon...
