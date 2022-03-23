********************
Protocol Description
********************

This section presents a description of the NGHam protocol, like packet format, data fields, configuration parameters and others. More information can also be found in the original documentation [1]_.

Overview
========

The NGHam protocol stands for *Next Generation Ham Radio*, being a protocol designed for packet communication. It is similar to the classical AX.25 [2]_ protocol, but with the idea of using a FEC (*Forwared Error Correction*) algorithm to increase the robustness, as defined in [3]_:

    "*...a link protocol partly inspired by AX.25. In order to improve the link reliability, it features Reed Solomon codes for Forward Error Correction (FEC). This makes the data transmission more robust compared to i.e. AX.25, which does not implement FEC on the link layer directly.*"

It was originally developed in the context of the CubeSat NUTS-1 (*NTNU Test Satellite*) development, by the Norwegian University of Science and Technology (NTNU). This library is based on the implementation of Jon Petter Skagmo (LA3JPA), available in [4]_.


Packet Fields
=============

The figure below presents a diagram with packet format and the data fields of the NGHam protocol.

.. figure:: ngham-pkt.png
      :width: 100%
      :align: center
      :alt: NGHam packet format

      Fig. Format of a NGHam packet.

Next, there is a brief description of each one of those fields.

Preamble
--------

Considering a data rate of 9600 bps, 4 bytes is typically used for the preamble. This sequence is an alternation of ones and zeros: :math:`4 \times` 0xAA (0b10101010).

Sync. Word
----------

The sync. word is a sequence of bits used for packet synchronization. With this sequence, the receiver can detect the start of a new packet. In NGHam, the sync. word is composed by 32 bits, following the pattern: 0x5D, 0xE6, 0x2A, 0x7E.

Size Tag
--------

This field indicates one of the seven possible packet sizes. It is a 24 bits tag and is made very robust by keeping a hamming distance of 13 bits between all vectors. The seven possible tags are listed below:

+---------------+---------------+--------------------------+-------------------------+
| **Size Num.** | **Tag**       | **Reed-Solomon Config.** | **Max. Data Size**      |
+---------------+---------------+--------------------------+-------------------------+
| 1             | 59, 73, 205   | RS(47, 31)               | up to 28 bytes of data  |
+---------------+---------------+--------------------------+-------------------------+
| 2             | 77, 218, 87   | RS(79, 63)               | up to 60 bytes of data  |
+---------------+---------------+--------------------------+-------------------------+
| 3             | 118, 147, 154 | RS(111, 95)              | up to 92 bytes of data  |
+---------------+---------------+--------------------------+-------------------------+
| 4             | 155, 180, 174 | RS(159, 127)             | up to 124 bytes of data |
+---------------+---------------+--------------------------+-------------------------+
| 5             | 160, 253, 99  | RS(191, 159)             | up to 156 bytes of data |
+---------------+---------------+--------------------------+-------------------------+
| 6             | 214, 110, 249 | RS(223, 191)             | up to 188 bytes of data |
+---------------+---------------+--------------------------+-------------------------+
| 7             | 237, 39, 52   | RS(255, 223)             | up to 220 bytes of data |
+---------------+---------------+--------------------------+-------------------------+

Reed-Solomon Block
------------------

The Reed-Solomon code block (or just RS block), is the field with packet payload and parity data. It is divided in two parts: data and parity bytes. The data bytes is subdivided in four different fields: header, payload, checksum and padding. Each one of these fields are described below.

Header
......

The header byte is the first data byte of the RS block. It is divided as presented in the table below.

+----------+-------------------------+
| **Bits** | **Purpose**             |
+----------+-------------------------+
| 7 to 6   | Reserved                |
+----------+-------------------------+
| 5        | Extension on            |
+----------+-------------------------+
| 4 to 0   | Padding size (in bytes) |
+----------+-------------------------+

The extension bit indicates if the extension frame is enabled or not. The padding size bits is the number padding bytes presented in the respective packet (0 to 31).

.. note::

   The extensions are not implemented yet on this library!

Payload
.......

The payload field is where the "useful" data of the packet is stored. As presented in the Size Tag field description above, each one of the seven size groups allow a certain maximum number of bytes in the packet payload. The maximum possible length of the payload for a NGHam packet is 220 bytes. If more data need to be transmitted, it should be divided in multiples chunks of 220 bytes, and transmitted in separated packets.

Checksum
........

To ensure data correctness and a first stage before running the Reed-Solomon correction algorithm, there is a checksum field after the payload data. The used checksum algorithm is the CRC16-CCITT [5]_, with the following configuration:

* **Polynomial**: 0x1021
* **Initial value**: 0xFFFF
* **Final XOR value**: 0xFFFF

The CRC16 value is computed from the header and the payload fields.

If the CRC16 value is correct, the Reed-Solomon chain is skipped and the packet is directly considered valid. This way, the checksum field also allows a performance improvement.

Padding
.......

To ensure the right packet length for the Reed-Solomon coding in use, if the payload content is less than the maximum allowed, the data field of the RS block is padded with zeros. The number of padding bytes is declared in the header byte (bits 4-0).

Parity Data
...........

This field is reserved for the computed parity bytes of the Reed-Solomon coding algorithm. The used implementation of the RS algorithm is based on the famous FEC library developed by Phil Karn (KA9Q) [6]_. This field can be 16 or 32 bytes long, depending on the payload length, and consequently, the adopted RS scheme:

+---------------+--------------------------+------------------+
| **Size Num.** | **Reed-Solomon Config.** | **Parity bytes** |
+---------------+--------------------------+------------------+
| 1             | RS(47, 31)               | 16               |
+---------------+--------------------------+------------------+
| 2             | RS(79, 63)               | 16               |
+---------------+--------------------------+------------------+
| 3             | RS(111, 95)              | 16               |
+---------------+--------------------------+------------------+
| 4             | RS(159, 127)             | 32               |
+---------------+--------------------------+------------------+
| 5             | RS(191, 159)             | 32               |
+---------------+--------------------------+------------------+
| 6             | RS(223, 191)             | 32               |
+---------------+--------------------------+------------------+
| 7             | RS(255, 233)             | 32               |
+---------------+--------------------------+------------------+

Scrambling
==========

Before transmitting a packet, the RS code block is scrambled by making a byte xor operation with a pre-generated table based on the polynomial :math:`x^{8} + x^{7} + x^{5} + x^{3} + 1` (defined in the CCSDS 131.0-B-3 standard [7]_).

When the receiver received a packet, it also perform the same operation to de-scramble the RS code block and get the original content of the RS part of the packet.

By scrambling the packets, long sequence of ones or zeros are avoided, by guarantying a good bit transition along the whole packet. More information about packet scrambling (or randomization) can be found in [7]_ (section 8.3).

.. [1] https://github.com/skagmo/ngham/blob/master/documentation/ngham_manual.pdf
.. [2] http://www.ax25.net/
.. [3] Løfaldli, André; Birkeland, Roger. *Implementation of a Software Defined Radio Prototype Ground Station for CubeSats*. The 4S Symposium 2016.
.. [4] https://github.com/skagmo/ngham
.. [5] https://en.wikipedia.org/wiki/ITU-T
.. [6] http://www.ka9q.net/code/fec/
.. [7] https://public.ccsds.org/Pubs/132x0b3.pdf
