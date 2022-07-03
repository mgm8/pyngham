#
# extension.py
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

from pyngham.pyngham import _PYNGHAM_PL_SIZES

class ExtPktType(Enum):
    """
    Extension packets types.
    """
    DATA          = 0
    ID            = 1
    STAT          = 2
    SIMPLEDIGI    = 3
    POS           = 4
    TOH           = 5
    DEST          = 6     # Destination/receiver callsign
    CMD_REQ       = 7     # Command packet
    CMD_REPLY     = 8     # Command packet
    REQUEST       = 9

_PYNGHAM_EXT_PKT_TYPES              = 10
_PYNGHAM_EXT_PKT_SIZE_VARIABLE      = 0xFFFF
_PYNGHAM_EXT_PKT_TYPE_SIZES         = [_PYNGHAM_EXT_PKT_SIZE_VARIABLE,
                                       7,   # ID
                                       22,  # Stat
                                       1,
                                       17,  # Pos
                                       5,   # Toh
                                       6,   # Dest
                                       _PYNGHAM_EXT_PKT_SIZE_VARIABLE,
                                       _PYNGHAM_EXT_PKT_SIZE_VARIABLE,
                                       1]

class PyNGHamExtension:
    """
    Class to handle NGHam extension packets.
    """

    def __init__(self):
        """
        Constructor.
        """
        pass

    def get_numpkts(self, d):
        """
        Gets the number of extension packets in a NGHam packet.

        :param d: is the packet payload with extension packet.

        :return The detected number of extension packets.
        """
        # Go through all sub packets
        start = int()
        packets = int()
        start = 0
        packets = 0
        d_len = len(d)

        while((d_len >= (start + 2)) and (d_len >= (start + 2 + d[start + 1]))):
            # If PKT_TYPE is invalid valid or packet type does not have correct length
            if ((d[start] > _PYNGHAM_EXT_PKT_TYPES) or  ((_PYNGHAM_EXT_PKT_TYPE_SIZES[d[start]] != _PYNGHAM_EXT_PKT_SIZE_VARIABLE) and (_PYNGHAM_EXT_PKT_TYPE_SIZES[d[start]] != d[start + 1]))):
                return 0
            packets += 1
            start += d[start + 1] + 2   # next start

        return packets

    def append_pkt(self, pl, typ, data):
        """
        Appends a new extension packet to a NGHam payload.

        :param pl: is the packet payload to append an extension packet.
        :param typ: is the type of extension packet.
        :param data: is the content of the extension packet.

        :return The given payload with the extension packet.
        """
        if len(pl) + 2 + len(data) > _PYNGHAM_PL_SIZES[-1]:
            return pl

        pl.append(typ)
        pl.append(len(data))
        pl = pl + data

        return pl

    def append_toh_pkt(self, pl, toh_us, toh_val):
        """
        Adds a TOH extension packet to a NGHam payload.

        :param pl is the packet payload to append a TOH packet:
        :param toh_us: time of hour in microseconds.
        :param toh_val: validity.

        :return The given payload with the new TOH extension packet.
        """
        data = list()

        data.append((toh_us >> 24) & 0xFF)
        data.append((toh_us >> 16) & 0xFF)
        data.append((toh_us >> 8) & 0xFF)
        data.append(toh_us & 0xFF)
        data.append(toh_val)

        return self.append_pkt(pl, ExtPktType.TOH.value, data)

    def append_stat_pkt(self, pl, hw_ver, serial, sw_ver, uptime_s, voltage, temp, signal, noise, cntr_rx_ok, cntr_rx_fix, cntr_rx_err, cntr_tx):
        """
        Adds an statistic extension packet to a NGHam payload.

        :param pl: is the packet payload to append an statistic packet.
        :param hw_ver: hardware version ID (10b for company, 6b for product).
        :param serial: Serial number.
        :param sw_ver: software version ID (4b major, 4b minor, 8b build).
        :param uptime_s: time in whole seconds since startup.
        :param voltage: input voltage in decivolts (0-25.5)
        :param temp: system temperature in degrees Celsius (-128 to 127).
        :param signal: received signal strength in dBm - 200, -200 to 54 (0xFF=N/A).
        :param noise: noise floor, same as above.
        :param cntr_rx_ok: packets successfully received.
        :param cntr_rx_fix: packets with corrected errors.
        :param cntr_rx_err: packets with uncorrectable errors.
        :param cntr_tx: packets sent.

        :return The given payload with the new statistic extension packet.
        """
        data = list()

        data.append((hw_ver >> 8) & 0xFF)
        data.append(hw_ver & 0xFF)
        data.append((serial >> 8) & 0xFF)
        data.append(serial & 0xFF)
        data.append((sw_ver >> 8) & 0xFF)
        data.append(sw_ver & 0xFF)
        data.append((uptime_s >> 24) & 0xFF)
        data.append((uptime_s >> 16) & 0xFF)
        data.append((uptime_s >> 8) & 0xFF)
        data.append(uptime_s & 0xFF)
        data.append(voltage)
        data.append(temp)
        data.append(signal)
        data.append(noise)
        data.append((cntr_rx_ok >> 8) & 0xFF)
        data.append(cntr_rx_ok & 0xFF)
        data.append((cntr_rx_fix >> 8) & 0xFF)
        data.append(cntr_rx_fix & 0xFF)
        data.append((cntr_rx_err >> 8) & 0xFF)
        data.append(cntr_rx_err & 0xFF)
        data.append((cntr_tx >> 8) & 0xFF)
        data.append(cntr_tx & 0xFF)

        return self.append_pkt(pl, ExtPktType.STAT.value, data)

    def append_pos_pkt(self, pl, latitude, longitude, altitude, sog, cog, hdop):
        """
        Adds a position extension packet to a NGHam payload.

        :param pl: is the packet payload to append a position packet.
        :param latitude: Latitude in degrees * 10^7
        :param longitude: Longitude in degrees * 10^7
        :param altitude: Altitude in centimeters
        :param sog: Hundreds of meters per second
        :param cog: Tenths of degrees
        :param hdop: In tenths

        :return The given payload with the new position extension packet.
        """
        data = list()

        data.append((latitude >> 24) & 0xFF)
        data.append((latitude >> 16) & 0xFF)
        data.append((latitude >> 8) & 0xFF)
        data.append(latitude & 0xFF)
        data.append((longitude >> 24) & 0xFF)
        data.append((longitude >> 16) & 0xFF)
        data.append((longitude >> 8) & 0xFF)
        data.append(longitude & 0xFF)
        data.append((altitude >> 24) & 0xFF)
        data.append((altitude >> 16) & 0xFF)
        data.append((altitude >> 8) & 0xFF)
        data.append(altitude & 0xFF)
        data.append((sog >> 8) & 0xFF)
        data.append(sog & 0xFF)
        data.append((cog >> 8) & 0xFF)
        data.append(cog & 0xFF)
        data.append(hdop)

        return self.append_pkt(pl, ExtPktType.POS.value, data)

    def append_id_pkt(self, pl, call_ssid, sequence):
        """
        Adds a ID extension packet to a NGHam payload.

        :note: Always first in a packet, except when resent by another station.

        :param pl: is the packet payload to append an ID packet.
        :param call_ssid: 7 x 6 bit (SIXBIT DEC, which is ASCII-32 and limited to 0-64) empty characters padded with 0, 6 bit SSID.
        :param sequence: is the packet sequence number, wraps around from 255 to 0.

        :return The given payload with the new ID extension packet.
        """
        data = list()

        data = data + call_ssid
        data.append(sequence)

        return self.append_pkt(pl, ExtPktType.ID.value, data)

    def append_dest_pkt(self, pl, call_ssid):
        """
        Adds a destination extension packet to a NGHam payload.

        :param pl: is the packet payload to append a destination packet.
        :param call_ssid: 7 x 6 bit (SIXBIT DEC, which is ASCII-32 and limited to 0-64) empty characters padded with 0, 6 bit SSID.

        :return The given payload with the new destination extension packet.
        """
        return self.append_pkt(pl, ExtPktType.DEST.value, call_ssid)

    def decode(self, pl):
        """
        Decodes all extension packets in a given NGHam payload.

        :param pl: is the NGHam payload to decode.

        :return All found extension packets as a list of dictionaries.
        """
        pass

    def encode_callsign(self, callsign):
        """
        Encodes a given callsign.

        :param callsign: is the callsign to encode (ASCII string).

        :return The encoded callsign as a list of integers (bytes).
        """
        callsign = list(callsign)
        enc_callsign = list()

        temp = int()
        j = 0
        copy = list(8*' ')
        ssid = 0

        # Convert to DEC SIXBIT until length is 7, zero terminated, or dash (SSID start)
        while(True):
            # Lowercase converted to uppercase
            if (ord(callsign[j]) >= 0x61) and (ord(callsign[j]) <= 0x7A):
                copy[j] = chr(ord(callsign[j]) - 64)
            else:
                copy[j] = chr(ord(callsign[j]) - 32)

            j += 1

            if (j < 7) and ord(callsign[j]) and (callsign[j] != '-'):
                break

        if j < 7:
            copy[j] = chr(0)    # Zero terminate if preliminary end

        # Get SSID, if any
        if callsign[j] == '-':
            j += 1
            # First number
            if (ord(callsign[j]) >= 0x30) and (ord(callsign[j]) <= 0x39):
                ssid += (ord(callsign[j]) - ord('0'))
            else:
                return list()
            j += 1
            # Second number
            if (ord(callsign[j]) >= 0x30) and (ord(callsign[j]) <= 0x39):
                ssid *= 10
                ssid += (ord(callsign[j]) - ord('0'))
                j += 1
            elif ord(callsign[j]) != 0:
                return list()

        temp = ((ord(copy[0]) << 18) & 0xFC0000) | ((ord(copy[1]) << 12) & 0x3F000) | ((ord(copy[2]) << 6) & 0xFC0) | (ord(copy[3]) & 0x3F)
        enc_callsign.append((temp >> 16) & 0xFF)
        enc_callsign.append((temp >> 8) & 0xFF)
        enc_callsign.append(temp & 0xFF)

        temp = ((ord(copy[4]) << 18) & 0xFC0000) | ((ord(copy[5]) << 12) & 0x3F000) | ((ord(copy[6]) << 6) & 0xFC0) | (ssid & 0x3F)
        enc_callsign.append((temp >> 16) & 0xFF)
        enc_callsign.append((temp >> 8) & 0xFF)
        enc_callsign.append(temp & 0xFF)

        return enc_callsign

    def decode_callsign(self, enc_callsign):
        """
        Decodes a given encoded callsign.

        :param enc_callsign: the encoded callsign to decode.

        :return The decoded callsign as an string.
        """
        callsign = list(8*' ')

        temp = ((enc_callsign[0] << 16) & 0xFF0000) | ((enc_callsign[1] << 8) & 0xFF00) | (enc_callsign[2] & 0xFF)
        callsign[0] = (temp >> 18) & 0x3F
        callsign[1] = (temp >> 12) & 0x3F
        callsign[2] = (temp >> 6) & 0x3F
        callsign[3] = temp & 0x3F

        temp = ((enc_callsign[3] << 16) & 0xFF0000) | ((enc_callsign[4] << 8) & 0xFF00) | (enc_callsign[5] & 0xFF)
        callsign[4] = (temp >> 18) & 0x3F
        callsign[5] = (temp >> 12) & 0x3F
        callsign[6] = (temp >> 6) & 0x3F
        callsign[7] = 0     # Zero terminate (needed if max length)

        # Find end of callsign and convert from DEC SIXBIT
        j = 0
        while (j < 7) and callsign[j]:
            callsign[j] = callsign[j] + 32
            j += 1

        # If non-zero SSID
        ssid = temp & 0x3F
        if ssid:
            callsign[j] = '-'
            j += 1
            if ssid > 9:
                callsign[j] = (ssid/10) + ord('0')
                j += 1
                ssid %= 10
            callsign[j] = ssid + ord('0')
            j += 1
            callsign[j] = 0

        return callsign
