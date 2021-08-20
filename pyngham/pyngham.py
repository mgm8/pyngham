#
# pyngham.py
# 
# Copyright (C) 2021, Gabriel Mariano Marcelino - PU5GMA <gabriel.mm8@gmail.com>
# 
# This file is part of PyNGHam library.
# 
# PyNGHamlibrary is free software: you can redistribute it and/or modify
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


from reedsolo import RSCodec

# There are seven different sizes
# Each size has a correlation tag for size, a total size, a maximum payload size and a parity data size
_PYNGHAM_SIZES                  = 7
_PYNGHAM_PL_SIZES               = [28, 60, 92,  124, 156, 188, 220]
_PYNGHAM_PL_SIZES_FULL          = [31, 63, 95,  127, 159, 191, 223]
_PYNGHAM_PL_PAR_SIZES           = [47, 79, 111, 159, 191, 223, 255]
_PYNGHAM_PL_PAR_SIZES           = [16, 16, 16,  32,  32,  32,  32]

# Decoder states
_PYNGHAM_STATE_SIZE_TAG         = 0
_PYNGHAM_STATE_SIZE_TAG_2       = 1
_PYNGHAM_STATE_SIZE_TAG_3       = 2
_PYNGHAM_STATE_SIZE_KNOWN       = 3
_PYNGHAM_STATE_STATUS           = 4
_PYNGHAM_STATE_STATUS_2         = 5

# The seven different size tag vectors
_PYNGHAM_SIZE_TAGS              = [0b001110110100100111001101,
                                   0b010011011101101001010111,
                                   0b011101101001001110011010,
                                   0b100110111011010010101110,
                                   0b101000001111110101100011,
                                   0b110101100110111011111001,
                                   0b111011010010011100110100]

# Maximum number of errors in the size tag
_PYNGHAM_SIZE_TAG_MAX_ERROR     = 6

# Preamble and synchronization vector
_PYNGHAM_PREAMBLE               = 0xAA
_PYNGHAM_SYNC_WORD              = [0x5D, 0xE6, 0x2A, 0x7E]
_PYNGHAM_PREAMBLE_FOUR_LEVEL    = 0xDD
_PYNGHAM_SYNC_WORD_FOUR_LEVEL   = [0x77, 0xF7, 0xFD, 0x7D, 0x5D, 0xDD, 0x7F, 0xFD]

# Reed Solomon control blocks for the different NGHam sizes
_PYNGHAM_RS_CB                  = list(_PYNGHAM_SIZES)

class PyNGHam:

    def __init__(self):
        self._decoder_state = _PYNGHAM_STATE_SIZE_TAG

    def __str__(self):

    def encode(self, pl):
        return list()

    def decode(self, pkt):
        return list()
