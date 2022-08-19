*****************
Extension Packets
*****************

If the NGHam extension flag is set, the Payload contains NGHam extension data. Each NGHam extension packet has a separate header, describing the type and size of the following data. A payload can contain multiple extension packets, each containing information such as position, callsign, timing information, statistics, destination, repeating information and others. Below there is a figure with a diagram illustrating the format of a NGHam Extension packet.

.. figure:: ngham-ext-pkt.png
      :width: 100%
      :align: center
      :alt: NGHam Extension packet

      Fig. Format of a NGHam Extension packet.

.. note::
   Since the extension packets are not fully implemented and documented in the original NGHam implementation, the support for this resource is not complete yet. Some extension packet are already implemented and working, and some are not implemented because of lack of information about it. In the future, a definition of these packets are planned to be done.

Types of Extension Packets
==========================

Next, there is a description of each kind of extension packet provided by the NGHam protocol.

Data Packet
-----------

TODO

ID Packet
---------

TODO

Status Packet
-------------

TODO

Simple Digipeater Packet
------------------------

TODO

Position Packet
---------------

TODO

Time Information Packet
-----------------------

TODO

Destination Packet
------------------

TODO

Command Request Packet
----------------------

TODO

Command Reply Packet
--------------------

TODO

Request Packet
--------------

TODO
