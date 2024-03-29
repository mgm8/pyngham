---
title: 'PyNGHam: A Python library of the NGHam protocol'
tags:
  - Python
  - Telecommunications
  - Protocols
  - Ham Radio
authors:
  - name: Gabriel Mariano Marcelino
    orcid: 0000-0003-4889-6021
    affiliation: "1, 2"
affiliations:
 - name: Space Technology Research Laboratory (SpaceLab), Universidade Federal de Santa Catarina
   index: 1
 - name: Senai Institute for Innovation in Embedded Systems (ISI-SE)
   index: 2
date: 29 November 2022
bibliography: paper.bib
---

# Summary

The PyNGHam library is a Python implementation of the original NGHam protocol library written in C by Jon Petter Skagmo (LA3JPA) [@ngham]. The NGHam protocol is an amateur radio protocol developed to be a modern version of the AX.25 protocol, with the main improvement of introducing a forward error correction (FEC) algorithm, which considerably improves the robustness of the communication link. One of the main applications of this protocol is on small satellite projects (specifically CubeSats), supporting a reliable communication link between the ground station and the satellite. This Python implementation enables easier integration and use of this protocol in computers and embedded devices.

# Statement of Need

The NGHam protocol was originally developed in the context of a CubeSat development at the Norwegian University of Science and Technology (NTNU) [@lofaldi2016]. It was later used by the Space Technology Research Laboratory (SpaceLab) team, from Universidade Federal de Santa Catarina (Brazil), on the FloripaSat-1 CubeSat, and is being used by all satellites of the group so far. The known satellites that have used or plan to use the NGHam protocol are:

* **FloripaSat-1** [@marcelino2020]
* **GOLDS-UFSC** (a.k.a. **FloripaSat-2**) [@golds-ufsc]
* **Catarina-A1** (Catarina Constellation) [@seman2022]
* **PION-BR1** [@pion-br1]
* **Aldebaran-1**
* **NUTS-1** [@lofaldi2016]

The first three satellites in the list are satellites developed (or in development) by the same research group, the SpaceLab, where this library was developed.

From the knowledge of the author, there is no Python implementation of the protocol in the literature. An implementation in a high-level language facilitates the development of user applications to communicate with objects in orbit. The intention is to make PyNGHam usable in end-user applications, like satellite decoders used in real satellite missions. It is an alternative to the GNU Radio [@gnu-radio] blocks such as gr-nuts [@gr-nuts], but independent from the GNU Radio ecosystem. It is also useful as a simulation or research/education tool that can be used in simple Python scripts.

This library is already being used in the design of satellites by SpaceLab, as a part of the ground station software [@spacelab-decoder; @spacelab-transmitter] responsible for the uplink of telecommands and downlink of telemetry/payload data.

# NGHam Protocol

The NGHam (Next Generation Ham Radio) protocol is a link protocol partly inspired by AX.25 [@ax25], with the intention to be used in Ham radio packet communications, but using a FEC algorithm on a well-defined packet structure.

For the FEC algorithm, the Reed-Solomon code (RS) is employed [@reed1960]. Figure \ref{fig:ngham-pkt} presents a diagram with the fields of a NGHam packet.

![Fields of a NGHam packet.\label{fig:ngham-pkt}](../docs/ngham-pkt.png)

For a GMSK (Gaussian Minimum - Shift Keying) modulation at 9600 bps, a typical preamble sequence would be `0xAAAAAAAA` (a simple alternate of ones and zeros).

The size tag field has seven different options, each corresponding to a unique packet size as described in Table 1.

----------------------------------------------------------------------
Size Num.   Tag             Reed-Solomon Config.    Max. Data Size
----------  --------------  ---------------------   ------------------
1           59, 73, 205     RS(47, 31)              28 bytes of data

2           77, 218, 87     RS(79, 63)              60 bytes of data

3           118, 147, 154   RS(111, 95)             92 bytes of data

4           155, 180, 174   RS(159, 127)            124 bytes of data

5           160, 253, 99    RS(191, 159)            156 bytes of data

6           214, 110, 249   RS(223, 191)            188 bytes of data

7           237, 39, 52     RS(255, 223)            220 bytes of data
----------------------------------------------------------------------

Table:  NGHam packets sizes.

Following the seven possible packet sizes, after the size tag field, there is the data field with the Reed-Solomon code block, with seven different schemes, one for each size tag. As can be seen in Figure \ref{fig:ngham-pkt}, the used RS configurations are: (47, 31), (79, 63), (111, 95), (159, 127), (191, 159), (223, 191), and (255, 223), respectively.

The code block consists of two types of fields: packet data and parity data. The parity data is the byte sequence generated by the Reed-Solomon algorithm. The packet data is the information presented in the packet and is divided into four fields: header, payload, CRC (Cyclic-Redundancy Code), and padding.

## Scrambling

Before transmitting a packet, the RS code block is scrambled by making a logical `xor` operation with a pre-generated table based on the polynomial $x^{8} + x^{7} + x^{5} + x^{3} + 1$ (defined in the CCSDS 131.0-B-4 standard, Section 10.4.1 [@ccsds]).

When the receiver receives a packet, it also performs the same operation to descramble the RS code block, ultimately retrieving the original content of the RS part of the packet. By scrambling the packets using the bit transition, long sequences of ones or zeros are mitigated (Section 8.3 of @ccsds).

## Serial Protocol

While the NGHam protocol can be used to support wireless communications, there is also the possibility to use the protocol in physical serial interfaces with a slightly different packet structure. In the serial protocol, no FEC algorithm is involved, but merely a checksum field to indicate whether an error occurred during the transmission can be integrated. Both wireless and serial options can be integrated into a device.

## Extensions

The payload of an NGHam packet can also contain subpackets, called extension packets. Each NGHam extension packet has a separate header describing the type and size of the subsequent data. A payload can contain multiple extension packets, each containing information such as position, callsign, timing information, statistics, destination, repeating information, and others. The use of extensions is optional.

# The Python Implementation

This Python implementation of the protocol was partly inspired by the structure of the original implementation in C, but with the main difference being the use of an object-oriented language. This way, a class for each of the three main possible uses of the protocol is available: the normal NGHam packets, the serial port packets, and the use of the extensions. All of these three classes are implemented with a similar approach, using at least two methods for packet encoding and decoding. The encoding and decoding processes generate a list of integers, representing the bytes of an NGHam packet/payload data. More information about the PyNGHam library can be found in the documentation: [https://mgm8.github.io/pyngham/](https://mgm8.github.io/pyngham/).


# Conclusion

The objective of this library is to offer an alternative to the original NGHam library, purely written in Python. In this manner, such a package can easily be used to carry out simulations, develop packet encoding and decoding tools, and introduce telecommunication concepts to students, among others. It is useful especially for satellite communications, space experiments, and for general use in the amateur radio community.

# Acknowledgements

The author would like to thank Jon Petter Skagmo (LA3JPA), the original creator of the protocol, Phil Karn (KA9Q), the developer of the FEC library, and the SpaceLab members for their support and feedback over the last years.

# References
