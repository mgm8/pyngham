#
# test_extension.py
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


import pyngham
from random import randrange

def test_extension_get_numpkts():
    ext = pyngham.PyNGHamExtension()

    pl = list()

    print(ext.encode_callsign("PU5GMA", 0))
    pl = ext.append_id_pkt(pl, ext.encode_callsign("PU5GMA", 0), 0)
    print(pl)

    assert ext.get_numpkts(pl) == 1

    pl = ext.append_dest_pkt(pl, ext.encode_callsign("PU5GMA", 1))
    print(pl)

    assert ext.get_numpkts(pl) == 2

    toh_us = randrange(2**16 - 1)
    toh_val = randrange(2**8 - 1)

    pl = ext.append_toh_pkt(pl, toh_us, toh_val)

    assert ext.get_numpkts(pl) == 3

def test_extension_toh_pkt():
    ext = pyngham.PyNGHamExtension()

    toh_us = randrange(2**16 - 1)
    toh_val = randrange(2**8 - 1)

    pl = list()

    pl = ext.append_toh_pkt(pl, toh_us, toh_val)

    assert pl == [5, 4 + 1, (toh_us >> 24) & 0xFF, (toh_us >> 16) & 0xFF, (toh_us >> 8) & 0xFF, toh_us & 0xFF, toh_val]

def test_extension_stat_pkt():
    ext = pyngham.PyNGHamExtension()

    hw_ver      = randrange(2**16 - 1)
    serial      = randrange(2**16 - 1)
    sw_ver      = randrange(2**16 - 1)
    uptime_s    = randrange(2**32 - 1)
    voltage     = randrange(2**8 - 1)
    temp        = randrange(2**7 - 1)
    signal      = randrange(2**8 - 1)
    noise       = randrange(2**8 - 1)
    cntr_rx_ok  = randrange(2**16 - 1)
    cntr_rx_fix = randrange(2**16 - 1)
    cntr_rx_err = randrange(2**16 - 1)
    cntr_tx     = randrange(2**16 - 1)

    pl = list()

    pl = ext.append_stat_pkt(pl, hw_ver, serial, sw_ver, uptime_s, voltage, temp, signal, noise, cntr_rx_ok, cntr_rx_fix, cntr_rx_err, cntr_tx)

    exp_pl = list()

    exp_pl.append(2)
    exp_pl.append(22)
    exp_pl.append((hw_ver >> 8) & 0xFF)
    exp_pl.append(hw_ver & 0xFF)
    exp_pl.append((serial >> 8) & 0xFF)
    exp_pl.append(serial & 0xFF)
    exp_pl.append((sw_ver >> 8) & 0xFF)
    exp_pl.append(sw_ver & 0xFF)
    exp_pl.append((uptime_s >> 24) & 0xFF)
    exp_pl.append((uptime_s >> 16) & 0xFF)
    exp_pl.append((uptime_s >> 8) & 0xFF)
    exp_pl.append(uptime_s & 0xFF)
    exp_pl.append(voltage)
    exp_pl.append(temp)
    exp_pl.append(signal)
    exp_pl.append(noise)
    exp_pl.append((cntr_rx_ok >> 8) & 0xFF)
    exp_pl.append(cntr_rx_ok & 0xFF)
    exp_pl.append((cntr_rx_fix >> 8) & 0xFF)
    exp_pl.append(cntr_rx_fix & 0xFF)
    exp_pl.append((cntr_rx_err >> 8) & 0xFF)
    exp_pl.append(cntr_rx_err & 0xFF)
    exp_pl.append((cntr_tx >> 8) & 0xFF)
    exp_pl.append(cntr_tx & 0xFF)

    assert pl == exp_pl

def test_extension_pos_pkt():
    ext = pyngham.PyNGHamExtension()

    latitude    = randrange(2**31 - 1)
    longitude   = randrange(2**31 - 1)
    altitude    = randrange(2**31 - 1)
    sog         = randrange(2**16 - 1)
    cog         = randrange(2**16 - 1)
    hdop        = randrange(2**8 - 1)

    pl = list()

    pl = ext.append_pos_pkt(pl, latitude, longitude, altitude, sog, cog, hdop)

    exp_pl = list()

    exp_pl.append(4)
    exp_pl.append(17)
    exp_pl.append((latitude >> 24) & 0xFF)
    exp_pl.append((latitude >> 16) & 0xFF)
    exp_pl.append((latitude >> 8) & 0xFF)
    exp_pl.append(latitude & 0xFF)
    exp_pl.append((longitude >> 24) & 0xFF)
    exp_pl.append((longitude >> 16) & 0xFF)
    exp_pl.append((longitude >> 8) & 0xFF)
    exp_pl.append(longitude & 0xFF)
    exp_pl.append((altitude >> 24) & 0xFF)
    exp_pl.append((altitude >> 16) & 0xFF)
    exp_pl.append((altitude >> 8) & 0xFF)
    exp_pl.append(altitude & 0xFF)
    exp_pl.append((sog >> 8) & 0xFF)
    exp_pl.append(sog & 0xFF)
    exp_pl.append((cog >> 8) & 0xFF)
    exp_pl.append(cog & 0xFF)
    exp_pl.append(hdop)

    assert pl == exp_pl

def test_extension_id_pkt():
    ext = pyngham.PyNGHamExtension()

    call_ssid = list()
    call_ssid.append(randrange(2**8 - 1))
    call_ssid.append(randrange(2**8 - 1))
    call_ssid.append(randrange(2**8 - 1))
    call_ssid.append(randrange(2**8 - 1))
    call_ssid.append(randrange(2**8 - 1))
    call_ssid.append(randrange(2**8 - 1))
    sequence = randrange(2**8 - 1)

    pl = list()

    pl = ext.append_id_pkt(pl, call_ssid, sequence)

    assert pl == [1, 7] + call_ssid + [sequence]

def test_extension_dest_pkt():
    ext = pyngham.PyNGHamExtension()

    call_ssid = list()
    call_ssid.append(randrange(2**8 - 1))
    call_ssid.append(randrange(2**8 - 1))
    call_ssid.append(randrange(2**8 - 1))
    call_ssid.append(randrange(2**8 - 1))
    call_ssid.append(randrange(2**8 - 1))
    call_ssid.append(randrange(2**8 - 1))

    pl = list()

    pl = ext.append_dest_pkt(pl, call_ssid)

    assert pl == [6, 6] + call_ssid

def test_extension_encode_callsign():
    ext = pyngham.PyNGHamExtension()

    callsign = "PU5GMA"
    ssid = 1

    dec_callsign, dec_ssid = ext.decode_callsign(ext.encode_callsign(callsign, ssid))

    assert (callsign == dec_callsign) and (ssid == dec_ssid)

def test_extension_decode_callsign():
    ext = pyngham.PyNGHamExtension()

    callsign = "PU5GMA"
    ssid = 1

    dec_callsign, dec_ssid = ext.decode_callsign(ext.encode_callsign(callsign, ssid))

    assert (callsign == dec_callsign) and (ssid == dec_ssid)
