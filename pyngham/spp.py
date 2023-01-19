#
# spp.py
# 
# Copyright (C) 2022, Gabriel Mariano Marcelino - PU5GMA <gabriel.mm8@gmail.com>
# 
# This file is part of PyNGHam library.
# 
# PyNGHam library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyNGHam library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with PyNGHam library. If not, see <http://www.gnu.org/licenses/>.
# 
#


from enum import Enum
import time
from crc import Calculator, Configuration

class SPPType(Enum):
    """
    Serial Port Protocol packets types:

    * **RX**: RF RX packet
    * **TX**: RF TX packet
    * **LOCAL**: Local packet
    * **CMD**: Command packet
    """
    RX      = 0             # RF RX packet
    TX      = 1             # RF TX packet
    LOCAL   = 2             # Local packet
    CMD     = 3             # Command packet

# Packet start byte definition
_PYNGHAM_SPP_START  = 0x24  # '$' in ASCII

class SPPState(Enum):
    """
    States:

    * **START**: Decoder in start flag field
    * **HEADER**: Decoder in header field
    * **PAYLOAD**: Decoder in payload field
    """
    START   = 0             # Decoder in start flag field
    HEADER  = 1             # Decoder in header field
    PAYLOAD = 2             # Decoder in payload field

_PYNGHAM_SPP_RX_BUFFER_MAX_SIZE = 1024


class PyNGHamSPP:
    """
    The protocol is used to transfer data and commands between the transceiver and the serial port host.
    """

    def __init__(self):
        """
        Class constructor.

        :return: None.
        :rtype: None
        """
        self._state = SPPState.START
        self._rx_buffer = list()

    def encode(self, pkt_type, pl):
        """
        Encodes a generic SPP packet from a given payload data. The SPP packets have the following fields:

        +----------------+-----------------+-------------------------------------------------------------+
        | **Name**       | **Size (Byte)** | **Notes**                                                   |
        +----------------+-----------------+-------------------------------------------------------------+
        | Start tag      |               1 | Fixed as ’$’.                                               |
        +----------------+-----------------+-------------------------------------------------------------+
        | CRC Size       |               2 | 16-bit CRC CCITT (start=0xffff, polynomial=0x1021 reversed, |
        |                |                 | Xorout=0xffff). Notice the use of little endian, as         |
        |                |                 | everything on this layer and up use little endian. CRC is   |
        |                |                 | calculated of everything except start tag and CRC itself.   |
        +----------------+-----------------+-------------------------------------------------------------+
        | Payload type   |               1 | 0x00=RF receive packet, 0x01=RF transmit packet,            |
        |                |                 | 0x02=Local packet, 0x03=Command.                            |
        +----------------+-----------------+-------------------------------------------------------------+
        | Payload length |               1 | Length of payload field.                                    |
        +----------------+-----------------+-------------------------------------------------------------+
        | Payload        |               n | This is the actual payload specified by the payload type.   |
        +----------------+-----------------+-------------------------------------------------------------+

        :param pkt_type: The SPP packet type (SPPType.RX.value, SPPType.TX.value, SPPType.LOCAL.value or SPPType.CMD.value).
        :type pkt_type: int

        :param pl: The payload of the desired SPP packet.
        :type pl: list[int]

        :return: The encoded SPP packet.
        :rtype: list[int]
        """
        if isinstance(pl, str):
            pl = [ord(x) for x in pl]
        pl = list(pl)   # Ensure that the input is a list of ints

        if len(pl) > (8 + 220):
            return list()

        pkt = list()

        # Payload type
        pkt.append(pkt_type)

        # Payload length
        pkt.append(len(pl))

        # Payload
        pkt = pkt + pl

        crc_val = Calculator(Configuration(16, 0x1021, 0xFFFF, 0xFFFF, True, True)).checksum(bytes(pkt))
        checksum = [(crc_val >> 8) & 0xFF, crc_val & 0xFF]

        # Start byte and CRC
        pkt = [_PYNGHAM_SPP_START] + checksum + pkt

        return pkt

    def encode_rx_pkt(self, noise_floor, rssi, symbol_errors, flags, data):
        """
        Encodes an RX packet from the given data.

        Data received from RF link. Length from 4 to 223. The table below describes what is put into the
        payload of the general packet format.

        +------------------------------+----------+------------------------------------------------------------+
        | **Name**                     | **Size** | **Notes**                                                  |
        +------------------------------+----------+------------------------------------------------------------+
        | Time of hour in microseconds |        4 | Local time of hour timestamp of the incoming packet.       |
        |                              |          | Wraps from 3599999999 (one step before 3600 seconds)       |
        |                              |          | to 0. N/A-value is 0xffffffff.                             |
        +------------------------------+----------+------------------------------------------------------------+
        | Noise floor                  |        1 | Subtract 200 to get dBm. Eg. 0x50 = -120 dBm. N/A is 0xff. |
        +------------------------------+----------+------------------------------------------------------------+
        | RSSI                         |        1 | Same as above.                                             |
        +------------------------------+----------+------------------------------------------------------------+
        | Symbol errors                |        1 | Number of corrected Reed-Solomon symbols.                  |
        +------------------------------+----------+------------------------------------------------------------+
        | Flags                        |        1 | Bit 0: NGHam extension enabled. If this bit is set, the    |
        |                              |          | data field is a valid NGHam extension packet.              |
        +------------------------------+----------+------------------------------------------------------------+
        | Data                         |      n-8 | Received data.                                             |
        +------------------------------+----------+------------------------------------------------------------+

        :param noise_floor: Noise floor value (see table above).
        :type noise_floor: int

        :param rssi: RSSI value (see table above).
        :type rssi: int

        :param symbol_errors: The number of corrected Reed-Solomon symbols.
        :type symbol_errors: int

        :param flags: RX packet flags (see table above).
        :type flags: int

        :param data: The data of the packet.
        :type data: list[int]

        :return: The encoded SPP RX packet.
        :rtype: list[int]
        """
        pl = list()

        ts = int(time.time())           # Timestamp (epoch)
        pl.append((ts >> 24) & 0xFF)
        pl.append((ts >> 16) & 0xFF)
        pl.append((ts >> 8) & 0xFF)
        pl.append(ts & 0xFF)
        pl.append(noise_floor + 200)    # Subtract 200 to get dBm. Eg. 0x50 = -120 dBm. N/A-value is 0xff
        pl.append(rssi + 200)           # Same as above
        pl.append(symbol_errors)        # Number of corrected Reed Solomon symbols
        pl.append(flags)                # Bit 0: NGHam extension enabled. If this bit is set, the data field is a valid NGHam extension packet

        return self.encode(SPPType.RX.value, pl + data)

    def encode_tx_pkt(self, flags, data):
        """
        Encodes a TX packet from the given data.

        Data to be transmitted on RF link. Length from 1 to 220. The table below describes what is put
        into the payload of the general packet format.

        +----------+-----------------+--------------------------------------+
        | **Name** | **Size (Byte)** | **Notes**                            |
        +----------+-----------------+--------------------------------------+
        | Flags    |               1 | Bit 0: NGHam extension enabled flag. |
        +----------+-----------------+--------------------------------------+
        | Data     |           n-1 B | Data to be transmitted.              |
        +----------+-----------------+--------------------------------------+

        :param flags: TX paket flags (see table above).
        :type flags: int

        :param data: The data of the packet.
        :type data: list[int]

        :return: The encoded SPP TX packet.
        :rtype: list[int]
        """
        return self.encode(SPPType.TX.value, [flags] + data)

    def encode_cmd_pkt(self, cmd):
        """
        Encodes a command packet.

        This type of packet is used to enter commands. On the Owl VHF, this command will do the same
        as typing into the command-line interpreter, except the commands and replies are not terminated
        by LF/CR/CRLF. The table below describes what is put into the payload of the general packet format.

        +----------+-----------------+-------------------------------------+
        | **Name** | **Size (Byte)** | **Notes**                           |
        +----------+-----------------+-------------------------------------+
        | Command  |             n B | Non-terminated command, 144800000”. |
        +----------+-----------------+-------------------------------------+

        :param cmd: A list with command content of the packet.
        :type cmd: int

        :return: The encoded SPP command packet.
        :rtype: list[int]
        """
        return self.encode(SPPType.CMD.value, cmd)

    def encode_local_pkt(self, flags, data):
        """
        Encodes a local packet.

        Packet generated by the radio (not received over the air). For example a status report. The table below describes what is put into the payload of the general packet format.

        +----------+-----------------+--------------------------------------+
        | **Name** | **Size (Byte)** | **Notes**                            |
        +----------+-----------------+--------------------------------------+
        | Flags    |               1 | Bit 0: NGHam extension enabled flag. |
        +----------+-----------------+--------------------------------------+
        | Data     |           n-1 B | Data to be transmitted.              |
        +----------+-----------------+--------------------------------------+

        :param flags: Local packet flags (see table above).
        :type flags: int

        :param data: The data of the local packet.
        :type data: list[int]

        :return: The encoded SPP local packet.
        :rtype: list[int]
        """
        return self.encode(SPPType.LOCAL.value, [flags] + data)

    def decode(self, pkt):
        """
        Decodes an SPP packet.

        :param pkt: is the SPP packet to decode.
        :type ptk: list[int]

        :return: The decoded packet as a dictionary.
        :rtype: dict
        """
        pkt = list(pkt)     # Ensure that the input is a list of ints
        for byte in pkt:
            dec_pkt = self.decode_byte(byte)
            if dec_pkt:
                return dec_pkt

        return dict()   # Error! Impossible to decode the packet!

    def decode_byte(self, c):
        """
        Decodes a single byte from a SPP packet.

        :param c: is the byte from a SPP packet to decode.
        :type c: int

        :return: An empty dictionary while the decoding is not done yet, and a dictionay with the decoded data when the decoding is ready.
        :rtype: dict
        """
        if self._state == SPPState.START:
            if c == _PYNGHAM_SPP_START:
                self._state = SPPState.HEADER
            self._rx_buffer = []
        elif self._state == SPPState.HEADER:
			# Fill RX buffer with header. No check for size, as buffer is much larger than header (5B)
            self._rx_buffer.append(c)

            if len(self._rx_buffer) >= 5:
                self._state = SPPState.PAYLOAD
        elif self._state == SPPState.PAYLOAD:
			# Fill RX buffer with payload
            if len(self._rx_buffer) < _PYNGHAM_SPP_RX_BUFFER_MAX_SIZE:
                self._rx_buffer.append(c)

			# If received length has met target length (set in STATE_HEADER)
            if len(self._rx_buffer) == (2 + 1 + 1 + self._rx_buffer[3]):
                # Check checksum
                crc_val = Calculator(Configuration(16, 0x1021, 0xFFFF, 0xFFFF, True, True)).checksum(bytes(self._rx_buffer[2:]))

                self._state = SPPState.START

                pkt = dict()

                if ((crc_val >> 8) == self._rx_buffer[0]) and ((crc_val & 0xFF) == self._rx_buffer[1]):
                    if self._rx_buffer[2] == SPPType.RX.value:
                        pkt = {
                            "type" :            self._rx_buffer[2],
                            "timestamp" :       (self._rx_buffer[4] << 24) | (self._rx_buffer[5] << 16) | (self._rx_buffer[6] << 8) | self._rx_buffer[7],
                            "noise_floor" :     self._rx_buffer[8] - 200,
                            "rssi" :            self._rx_buffer[9] - 200,
                            "symbol_errors" :   self._rx_buffer[10],
                            "flags" :           self._rx_buffer[11],
                            "payload" :         self._rx_buffer[12:]
                        }
                    elif self._rx_buffer[2] == SPPType.TX.value:
                        pkt = {
                            "type" :            self._rx_buffer[2],
                            "flags" :           self._rx_buffer[4],
                            "payload" :         self._rx_buffer[5:]
                        }
                    elif self._rx_buffer[2] == SPPType.LOCAL.value:
                        pkt = {
                            "type" :            self._rx_buffer[2],
                            "flags" :           self._rx_buffer[4],
                            "payload" :         self._rx_buffer[5:]
                        }
                    elif self._rx_buffer[2] == SPPType.CMD.value:
                        pkt = {
                            "type" :            self._rx_buffer[2],
                            "payload" :         self._rx_buffer[4:]
                        }
                    else:
                        pkt = {
                            "type" :            self._rx_buffer[2],
                            "payload" :         self._rx_buffer[4:]
                        }

                return pkt
        else:
            self._state = SPPState.START  # Unexpected, return to start state

        return dict()
