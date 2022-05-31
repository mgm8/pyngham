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


class PyNGHamExtension:

    def __init__(self):
        pass

    def numpkts(self, d):
        pass

    def encode_callsign(self, callsign):
        pass

    def decode_callsign(self, enc_callsign):
        pass
