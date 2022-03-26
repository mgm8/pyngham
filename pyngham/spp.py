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


# Seria Port Protocol packets types
_PYNGHAM_SPP_TYPE_RX            = 0
_PYNGHAM_SPP_TYPE_TX            = 1
_PYNGHAM_SPP_TYPE_LOCAL         = 2
_PYNGHAM_SPP_TYPE_CMD           = 3

# Packet start byte definition
_PYNGHAM_SPP_START              = 0x24

# States
_PYNGHAM_SPP_STATE_START        = 0
_PYNGHAM_SPP_STATE_HEADER       = 1
_PYNGHAM_SPP_STATE_PAYLOAD      = 2


class PyNGHamSPP:

    def __init__(self):
        pass

    def encode(self, pl, pkt_type, flags):
        pass

    def decode(self, pkt):
        pass

    def decode_byte(self, c):
        pass
