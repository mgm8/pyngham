#
# test_spp.py
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

def test_spp_pkt():
    spp = pyngham.PyNGHamSPP()

    pl = list()
    for i in range(randrange(220)):
        pl.append(randrange(256))

    # RX SPP packet
    noise_floor = randrange(-50, 0)
    rssi = randrange(-100, 30)
    errors = randrange(16)
    flags = 0
    rx_pkt = spp.encode_rx_pkt(noise_floor, rssi, errors, flags, pl)

    data = spp.decode(rx_pkt)

    assert data["type"] == pyngham.PYNGHAM_SPP_TYPE_RX
    assert data["noise_floor"] == noise_floor
    assert data["rssi"] == rssi
    assert data["symbol_errors"] == errors
    assert data["flags"] == flags
    assert data["payload"] == pl

    # TX packet
    flags = 0
    tx_pkt = spp.encode_tx_pkt(flags, pl)

    data = spp.decode(tx_pkt)

    assert data["type"] == pyngham.PYNGHAM_SPP_TYPE_TX
    assert data["flags"] == flags
    assert data["payload"] == pl

    # CMD packet
    cmd_pkt = spp.encode_cmd_pkt(pl)

    data = spp.decode(cmd_pkt)

    assert data["type"] == pyngham.PYNGHAM_SPP_TYPE_CMD
    assert data["payload"] == pl

    # Local packet
    flags = 0
    local_pkt = spp.encode_local_pkt(flags, pl)

    data = spp.decode(local_pkt)

    assert data["type"] == pyngham.PYNGHAM_SPP_TYPE_LOCAL
    assert data["flags"] == flags
    assert data["payload"] == pl
