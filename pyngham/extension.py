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

    * **DATA**: Generic data packet
    * **ID**: ID packet
    * **STAT**: Status packet
    * **SIMPLEDIGI**: Simple digi packet
    * **POS**: Position data packet
    * **TOH**: Time info packet
    * **DEST**: Destination/receiver callsign
    * **CMD_REQ**: Command request packet
    * **CMD_REPLY**: Command reply packet
    * **REQUEST**: Request packet
    """
    DATA          = 0       # Generic data packet
    ID            = 1       # ID packet
    STAT          = 2       # Status packet
    SIMPLEDIGI    = 3       # Simple digi packet
    POS           = 4       # Position data packet
    TOH           = 5       # Time info packet
    DEST          = 6       # Destination/receiver callsign
    CMD_REQ       = 7       # Command request packet
    CMD_REPLY     = 8       # Command reply packet
    REQUEST       = 9       # Request packet

_PYNGHAM_EXT_PKT_TYPES              = 10
_PYNGHAM_EXT_PKT_SIZE_VARIABLE      = 0xFFFF
_PYNGHAM_EXT_PKT_TYPE_SIZES         = [_PYNGHAM_EXT_PKT_SIZE_VARIABLE, 9, 22, 1, 17, 5, 8, _PYNGHAM_EXT_PKT_SIZE_VARIABLE, _PYNGHAM_EXT_PKT_SIZE_VARIABLE, 1]

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

        :param d: is the packet payload with extension packet(s).
        :type d: list[int]

        :return: The detected number of extension packets.
        :rtype: int
        """
        # Go through all sub packets
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
        :type pl: list[int]

        :param typ: is the type of extension packet.
        :type typ: int

        :param data: is the content of the extension packet.
        :type data: list[int]

        :return: The given payload with the extension packet.
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
        :type pl: list[int]

        :param toh_us: time of hour in microseconds.
        :type toh_us: int

        :param toh_val: validity.
        :type toh_val: int

        :return: The given payload with the new TOH extension packet.
        :rtype: list[int]
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
        :type pl: list[int]

        :param hw_ver: hardware version ID (10b for company, 6b for product).
        :type hw_ver: int

        :param serial: Serial number.
        :type serial: int

        :param sw_ver: software version ID (4b major, 4b minor, 8b build).
        :type sw_ver: int

        :param uptime_s: time in whole seconds since startup.
        :type uptime_s: int

        :param voltage: input voltage in decivolts (0-25.5)
        :type voltage: int

        :param temp: system temperature in degrees Celsius (-128 to 127).
        :type temp: int

        :param signal: received signal strength in dBm - 200, -200 to 54 (0xFF=N/A).
        :type signal: int

        :param noise: noise floor, same as above.
        :type noise: int

        :param cntr_rx_ok: packets successfully received.
        :type cntr_rx_ok: int

        :param cntr_rx_fix: packets with corrected errors.
        :type cntr_rx_fix: int

        :param cntr_rx_err: packets with uncorrectable errors.
        :type cntr_rx_err: int

        :param cntr_tx: packets sent.
        :type cntr_tx: int

        :return: The given payload with the new statistic extension packet.
        :rtype: list[int]
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
        :type pl: list[int]

        :param latitude: Latitude in degrees * 10^7
        :type latitude: int

        :param longitude: Longitude in degrees * 10^7
        :type longitude: int

        :param altitude: Altitude in centimeters
        :type altitude: int

        :param sog: Hundreds of meters per second
        :type sog: int

        :param cog: Tenths of degrees
        :type cog: int

        :param hdop: In tenths
        :type hdop: int

        :return: The given payload with the new position extension packet.
        :rtype: list[int]
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
        :type pl: list[int]

        :param call_ssid: 7 x 6 bit (SIXBIT DEC, which is ASCII-32 and limited to 0-64) empty characters padded with 0, 6 bit SSID.
        :type call_ssid: list[int]

        :param sequence: is the packet sequence number, wraps around from 255 to 0.
        :type sequence: int

        :return: The given payload with the new ID extension packet.
        :rtype: list[int]
        """
        data = list()

        data = data + call_ssid
        data.append(sequence)

        return self.append_pkt(pl, ExtPktType.ID.value, data)

    def append_dest_pkt(self, pl, call_ssid):
        """
        Adds a destination extension packet to a NGHam payload.

        :param pl: is the packet payload to append a destination packet.
        :type pl: list[int]

        :param call_ssid: 7 x 6 bit (SIXBIT DEC, which is ASCII-32 and limited to 0-64) empty characters padded with 0, 6 bit SSID.
        :type call_ssid: list[int]

        :return: The given payload with the new destination extension packet.
        :rtype: list[int]
        """
        return self.append_pkt(pl, ExtPktType.DEST.value, call_ssid)

    def decode(self, pl):
        """
        Decodes all extension packets in a given NGHam payload.

        :param pl: is the NGHam payload to decode.
        :type pl: list[int]

        :return: All found extension packets as a list of dictionaries.
        :rtype: dict
        """
        res = list()

        i = 0
        while(i < len(pl)):
            if pl[i] == ExtPktType.DATA.value:
                res.append(self._decode_data_pkt(pl[i + 2:i + pl[i+1] + 1]))
            elif pl[i] == ExtPktType.ID.value:
                res.append(self._decode_id_pkt(pl[i + 2:i + pl[i+1] + 1]))
            elif pl[i] == ExtPktType.STAT.value:
                res.append(self._decode_data_pkt(pl[i + 2:i + pl[i+1] + 1]))
            elif pl[i] == ExtPktType.SIMPLEDIGI.value:
                #res.append(self._decode_id_pkt(pl[i + 2:i + pl[i+1] + 1]))
                continue
            elif pl[i] == ExtPktType.POS.value:
                res.append(self._decode_stat_pkt(pl[i + 2:i + pl[i+1] + 1]))
            elif pl[i] == ExtPktType.TOH.value:
                res.append(self._decode_digi_pkt(pl[i + 2:i + pl[i+1] + 1]))
            elif pl[i] == ExtPktType.DEST.value:
                res.append(self._decode_pos_pkt(pl[i + 2:i + pl[i+1] + 1]))
            elif pl[i] == ExtPktType.CMD_REQ.value:
                #res.append(self._decode_cmd_req_pkt(pl[i + 2:i + pl[i+1] + 1]))
                continue
            elif pl[i] == ExtPktType.CMD_REPLY.value:
                #res.append(self._decode_cmd_reply_pkt(pl[i + 2:i + pl[i+1] + 1]))
                continue
            elif pl[i] == ExtPktType.REQUEST.value:
                #res.append(self._decode_request_pkt(pl[i + 2:i + pl[i+1] + 1]))
                continue
            else:
                continue

            i = i + 2 + pl[i+1]

        return res

    def _decode_data_pkt(self, pkt):
        """
        Decodes a data paketc.

        :param pkt: is the data packet to decode.
        :type pkt: list[int]

        :return: None
        :rtype: None
        """
        pass

    def _decode_id_pkt(self, pkt):
        """
        Decodes an ID packet.

        :param pkt: is the ID packet to decode.
        :type pkt: list[int]

        :return: None
        :rtype: None
        """
        res = {
            "call_ssid":    self.decode_callsign(pkt),
            "sequence":     pkt[-1]
            }

        return res

    def _decode_stat_pkt(self, pkt):
        """
        Decodes an status packet.

        :param pkt: is the status packet to decode.
        :type pkt: list[int]

        :return: A dictionary containing the fields of the decoded stat packet.
        :rtype: dict
        """
        res = {
            "hw_ver":       (pkt[0] << 8) | pkt[1],
            "serial":       (pkt[2] << 8) | pkt[3],
            "sw_ver":       (pkt[4] << 8) | pkt[5],
            "uptime_s":     (pkt[6] << 24) | (pkt[7] << 16) | (pkt[8] << 8) | pkt[9],
            "voltage":      pkt[10],
            "temp":         pkt[11],
            "signal":       pkt[12],
            "noise":        pkt[13],
            "cntr_rx_ok":   (pkt[14] << 8) | pkt[15],
            "cntr_rx_fix":  (pkt[16] << 8) | pkt[17],
            "cntr_rx_err":  (pkt[18] << 8) | pkt[19],
            "cntr_tx":      (pkt[20] << 8) | pkt[21],
            }

        return res

    def _decode_digi_pkt(self, pkt):
        pass

    def _decode_pos_pkt(self, pkt):
        """
        Decodes a position packet.

        :param pkt: is the position packet to decode.
        :type pkt: list[int]

        :return: A dictionary containing the fields of the decoded pos packet.
        :rtype: dict
        """
        res = {
            "latitude":     (pkt[0] << 24) | (pkt[1] << 16) | (pkt[2] << 8) | pkt[3],
            "longitude":    (pkt[4] << 24) | (pkt[4] << 16) | (pkt[5] << 8) | pkt[6],
            "altitude":     (pkt[7] << 24) | (pkt[8] << 16) | (pkt[9] << 8) | pkt[10],
            "sog":          (pkt[11] << 8) | pkt[12],
            "cog":          (pkt[13] << 8) | pkt[14],
            "hdop":         pkt[15]
            }

        return res

    def _decode_toh_pkt(self, pkt):
        """
        Decodes a TOH packet.

        :param pkt: is the TOH packet to decode.
        :type pkt: list[int]

        :return: A dictionary containing the fields of the decoded toh packet.
        :rtype: dict
        """
        res = {
            "toh_us":       (pkt[0] << 24) | (pkt[1] << 16) | (pkt[2] << 8) | pkt[3],
            "toh_val":      pkt[4]
            }

        return res

    def _decode_dest_pkt(self, pkt):
        """
        Decodes a destination packet.

        :param pkt: is the destination packet to decode.
        :type pkt: list[int]

        :return: A dictionary containing the fields of the decoded dest packet.
        :rtype: dict
        """
        res = {
            "call_ssid":    self.decode_callsign(pkt)
            }

        return res

    def _decode_cmd_req_pkt(self, pkt):
        pass

    def _decode_cmd_reply_pkt(self, pkt):
        pass

    def _decode_request_pkt(self, pkt):
        pass

    def encode_callsign(self, callsign, ssid):
        """
        Encodes a given callsign.

        :param callsign: is the callsign to encode (ASCII string).
        :type callsign: str

        :param ssid: is the SSID to encode with the callsign (integer).
        :type ssid: int

        :return: The encoded callsign as a list of integers (bytes).
        :rtype: list[int]
        """
        if (len(callsign) > 7) or (ssid >= 100):
            return list()

        # Convert to uppercase
        callsign = callsign.upper()

        # Convert to list of characters
        callsign = list(callsign)

        enc_callsign = list()

        for i in callsign:
            enc_callsign.append(ord(i))

        for i in range(7 - len(callsign)):
            enc_callsign.append(ord(' '))

        enc_callsign.append(ssid)

        return enc_callsign

    def decode_callsign(self, enc_callsign):
        """
        Decodes a given encoded callsign.

        :param enc_callsign: the encoded callsign to decode.
        :type enc_callsign: list[int]

        :return: The decoded callsign as an string.
        :rtype: str
        """
        callsign = str()

        for i in range(7):
            if enc_callsign[i] != ord(' '):
                callsign = callsign + chr(enc_callsign[i])

        return callsign, enc_callsign[-1]
