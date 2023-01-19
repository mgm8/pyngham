#
# pyngham.py
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
from crc import Calculator, Configuration
from pyngham.rs import RS

# There are seven different sizes
# Each size has a correlation tag for size, a total size, a maximum payload size and a parity data size
_PYNGHAM_SIZES                  = 7
_PYNGHAM_PL_SIZES               = [28, 60, 92,  124, 156, 188, 220]
_PYNGHAM_PL_SIZES_FULL          = [31, 63, 95,  127, 159, 191, 223]
_PYNGHAM_PL_PAR_SIZES           = [47, 79, 111, 159, 191, 223, 255]
_PYNGHAM_PAR_SIZES              = [16, 16, 16,  32,  32,  32,  32]

class State(Enum):
    """
    Decoder states:

    * **SIZE_TAG**
    * **SIZE_TAG_2**
    * **SIZE_TAG_3**
    * **SIZE_KNOWN**
    * **STATUS**
    * **STATUS_2**
    """
    SIZE_TAG         = 0
    SIZE_TAG_2       = 1
    SIZE_TAG_3       = 2
    SIZE_KNOWN       = 3
    STATUS           = 4
    STATUS_2         = 5

# The seven different size tag vectors
_PYNGHAM_SIZE_TAGS              = [[0x3B, 0x49, 0xCD],
                                   [0x4D, 0xDA, 0x57],
                                   [0x76, 0x93, 0x9A],
                                   [0x9B, 0xB4, 0xAE],
                                   [0xA0, 0xFD, 0x63],
                                   [0xD6, 0x6E, 0xF9],
                                   [0xED, 0x27, 0x34]]

# Maximum number of errors in the size tag
_PYNGHAM_SIZE_TAG_MAX_ERROR     = 6

# Preamble and synchronization vector
_PYNGHAM_PREAMBLE               = 4*[0xAA]
_PYNGHAM_SYNC_WORD              = [0x5D, 0xE6, 0x2A, 0x7E]
_PYNGHAM_PREAMBLE_FOUR_LEVEL    = 8*[0xDD]
_PYNGHAM_SYNC_WORD_FOUR_LEVEL   = [0x77, 0xF7, 0xFD, 0x7D, 0x5D, 0xDD, 0x7F, 0xFD]

# Repeats after 255 bits, but repeats byte-aligning after 255 byte
_PYNGHAM_CCSDS_POLY             = [0xFF, 0x48, 0x0E, 0xC0, 0x9A, 0x0D, 0x70, 0xBC, 0x8E, 0x2C, 0x93, 0xAD, 0xA7,
                                   0xB7, 0x46, 0xCE, 0x5A, 0x97, 0x7D, 0xCC, 0x32, 0xA2, 0xBF, 0x3E, 0x0A, 0x10,
                                   0xF1, 0x88, 0x94, 0xCD, 0xEA, 0xB1, 0xFE, 0x90, 0x1D, 0x81, 0x34, 0x1A, 0xE1,
                                   0x79, 0x1C, 0x59, 0x27, 0x5B, 0x4F, 0x6E, 0x8D, 0x9C, 0xB5, 0x2E, 0xFB, 0x98,
                                   0x65, 0x45, 0x7E, 0x7C, 0x14, 0x21, 0xE3, 0x11, 0x29, 0x9B, 0xD5, 0x63, 0xFD,
                                   0x20, 0x3B, 0x02, 0x68, 0x35, 0xC2, 0xF2, 0x38, 0xB2, 0x4E, 0xB6, 0x9E, 0xDD,
                                   0x1B, 0x39, 0x6A, 0x5D, 0xF7, 0x30, 0xCA, 0x8A, 0xFC, 0xF8, 0x28, 0x43, 0xC6,
                                   0x22, 0x53, 0x37, 0xAA, 0xC7, 0xFA, 0x40, 0x76, 0x04, 0xD0, 0x6B, 0x85, 0xE4,
                                   0x71, 0x64, 0x9D, 0x6D, 0x3D, 0xBA, 0x36, 0x72, 0xD4, 0xBB, 0xEE, 0x61, 0x95,
                                   0x15, 0xF9, 0xF0, 0x50, 0x87, 0x8C, 0x44, 0xA6, 0x6F, 0x55, 0x8F, 0xF4, 0x80,
                                   0xEC, 0x09, 0xA0, 0xD7, 0x0B, 0xC8, 0xE2, 0xC9, 0x3A, 0xDA, 0x7B, 0x74, 0x6C,
                                   0xE5, 0xA9, 0x77, 0xDC, 0xC3, 0x2A, 0x2B, 0xF3, 0xE0, 0xA1, 0x0F, 0x18, 0x89,
                                   0x4C, 0xDE, 0xAB, 0x1F, 0xE9, 0x01, 0xD8, 0x13, 0x41, 0xAE, 0x17, 0x91, 0xC5,
                                   0x92, 0x75, 0xB4, 0xF6, 0xE8, 0xD9, 0xCB, 0x52, 0xEF, 0xB9, 0x86, 0x54, 0x57,
                                   0xE7, 0xC1, 0x42, 0x1E, 0x31, 0x12, 0x99, 0xBD, 0x56, 0x3F, 0xD2, 0x03, 0xB0,
                                   0x26, 0x83, 0x5C, 0x2F, 0x23, 0x8B, 0x24, 0xEB, 0x69, 0xED, 0xD1, 0xB3, 0x96,
                                   0xA5, 0xDF, 0x73, 0x0C, 0xA8, 0xAF, 0xCF, 0x82, 0x84, 0x3C, 0x62, 0x25, 0x33,
                                   0x7A, 0xAC, 0x7F, 0xA4, 0x07, 0x60, 0x4D, 0x06, 0xB8, 0x5E, 0x47, 0x16, 0x49,
                                   0xD6, 0xD3, 0xDB, 0xA3, 0x67, 0x2D, 0x4B, 0xBE, 0xE6, 0x19, 0x51, 0x5F, 0x9F,
                                   0x05, 0x08, 0x78, 0xC4, 0x4A, 0x66, 0xF5, 0x58]

_PYNGHAM_PADDING_BM             = 0x1F
_PYNGHAM_FLAGS_BM               = 0xE0
_PYNGHAM_FLAGS_BP               = 5


class PyNGHam:
    """
    PyNGHam main class.

    This class is used to encode and/or decode a NGHam packet.
    """

    def __init__(self, mod=0):
        """
        Class initialization.

        This method initializes the seven Reed-Solomon schemes used by the NGHam protocol. After that, the encode and decode functions are ready to be used.

        :param mod: Modulation type (two=0 or four level=1, default 0).
        :type mod: int, optional

        :return: None.
        :rtype: None
        """
        self._modulation = mod

        self._decoder_size_nr = int()
        self._decoder_size_tag = int()
        self._decoder_state = State.SIZE_TAG.value
        self._decoder_buf = list()

        self._rsc = list()
        self._rsc.append(RS(8, 0x187, 112, 11, 16, _PYNGHAM_PL_PAR_SIZES[-1] - _PYNGHAM_PL_PAR_SIZES[0]))
        self._rsc.append(RS(8, 0x187, 112, 11, 16, _PYNGHAM_PL_PAR_SIZES[-1] - _PYNGHAM_PL_PAR_SIZES[1]))
        self._rsc.append(RS(8, 0x187, 112, 11, 16, _PYNGHAM_PL_PAR_SIZES[-1] - _PYNGHAM_PL_PAR_SIZES[2]))
        self._rsc.append(RS(8, 0x187, 112, 11, 32, _PYNGHAM_PL_PAR_SIZES[-1] - _PYNGHAM_PL_PAR_SIZES[3]))
        self._rsc.append(RS(8, 0x187, 112, 11, 32, _PYNGHAM_PL_PAR_SIZES[-1] - _PYNGHAM_PL_PAR_SIZES[4]))
        self._rsc.append(RS(8, 0x187, 112, 11, 32, _PYNGHAM_PL_PAR_SIZES[-1] - _PYNGHAM_PL_PAR_SIZES[5]))
        self._rsc.append(RS(8, 0x187, 112, 11, 32, _PYNGHAM_PL_PAR_SIZES[-1] - _PYNGHAM_PL_PAR_SIZES[6]))

    def __str__(self):
        """
        Represents the class as a string.

        :return: a brief description of the class.
        :rtype: str
        """
        return 'NGHam Protocol Handler'

    def _tag_check(self, x, y):
        """
        Verifies if a size tag is valid or not.

        :param x: Tag reference to compare.
        :type x: int

        :param y: Tag sequence to verify.
        :type y: int

        :return: True/False if the tag comparison passed or not.
        :rtype: bool
        """
        j = int()
        distance = int()
        diff = x ^ y

        # Early check to save time
        if not diff:
            return True

        distance = 0
        for j in range(24):
            if diff & 0x01:
                distance = distance + 1
                if distance > _PYNGHAM_SIZE_TAG_MAX_ERROR:
                    return False
            diff = diff >> 1

        return True

    def encode(self, pl, flags=0):
        """
        Encodes a sequence of bytes as a NGHam packet.

        :param pl: Data to encode as a NGHam packet (list of integeres, byte array or string).
        :type pl: list[int], bytearray or str

        :param flags: Packet flags, default 0.
        :type flags: int, optional

        :return: An encoded NGHam packet.
        :rtype: list[int]
        """
        if isinstance(pl, str):
            pl = [ord(x) for x in pl]
        pl = list(pl)   # Ensure that the input is a list of ints
        pkt = list()
        size_nr = 0
        codeword_start = 0

        # Check size and find control block for smallest possible RS codeword
        if (len(pl) == 0) or (len(pl) > _PYNGHAM_PL_SIZES[_PYNGHAM_SIZES-1]):
            return list()   # The given payload is greater than 220 bytes

        while(len(pl) > _PYNGHAM_PL_SIZES[size_nr]):
            size_nr = size_nr + 1

        # Insert preamble and sync word
        if self._modulation == 0:
            codeword_start = len(_PYNGHAM_PREAMBLE) + len(_PYNGHAM_SYNC_WORD) + len(_PYNGHAM_SIZE_TAGS[0])
            pkt = pkt + _PYNGHAM_PREAMBLE
            pkt = pkt + _PYNGHAM_SYNC_WORD
        else:
            codeword_start = len(_PYNGHAM_PREAMBLE_FOUR_LEVEL) + len(_PYNGHAM_SYNC_WORD_FOUR_LEVEL) + len(_PYNGHAM_SIZE_TAGS[0])
            pkt = pkt + _PYNGHAM_PREAMBLE_FOUR_LEVEL
            pkt = pkt + _PYNGHAM_SYNC_WORD_FOUR_LEVEL

        # Insert size tag
        pkt = pkt + _PYNGHAM_SIZE_TAGS[size_nr]

        # Insert header
        pkt = pkt + [((_PYNGHAM_PL_SIZES[size_nr] - len(pl)) & 0x1F) | ((flags << 5) & 0xE0)]

        # Insert payload
        pkt = pkt + pl

        # Insert checksum
        checksum = Calculator(Configuration(16, 0x1021, 0xFFFF, 0xFFFF, True, True)).checksum(bytes(pkt[codeword_start:]))
        pkt = pkt + [(checksum >> 8) & 0xFF, checksum & 0xFF]

        # Insert padding
        pkt = pkt + (_PYNGHAM_PL_SIZES_FULL[size_nr]-len(pl)-3)*[0x00]

        # Insert parity data
        pkt = pkt + self._rsc[size_nr].encode(pkt[codeword_start:])

        # Scramble
        for i in range(_PYNGHAM_PL_PAR_SIZES[size_nr]):
            pkt[codeword_start+i] = pkt[codeword_start+i] ^ _PYNGHAM_CCSDS_POLY[i]

        return pkt

    def decode(self, pkt):
        """
        Decodes a NGHam packet.

        :param pkt: raw NGHam packet to decode.
        :type pkt: list[int], bytearray or str

        :return: The decoded data, the number of corrected errors and a list with the bit position of the errors.
        :rtype: list[int], int, list[int]
        """
        pkt = list(pkt)     # Ensure that the input is a list of ints
        # Remove preamble and sync word if present
        if pkt[:8] == _PYNGHAM_PREAMBLE + _PYNGHAM_SYNC_WORD:
            pkt = pkt[8:]
        elif pkt[:16] == _PYNGHAM_PREAMBLE_FOUR_LEVEL + _PYNGHAM_SYNC_WORD_FOUR_LEVEL:
            pkt = pkt[16:]

        for byte in pkt:
            pl, errors, err_pos = self.decode_byte(byte)
            if len(pl) > 0:
                return pl, errors, err_pos

        return list(), -1, list()   # -1 = Error! Impossible to decode the packet!

    def decode_byte(self, byte):
        """
        Decodes a single byte from a NGHam packet.

        This function returns the decoded packet when the complete sequence of bytes is received.

        :param byte: byte of a raw NGHam packet to decode.
        :type byte: int

        :return: The decoded data, the number of corrected errors and a list with the bit position of the errors (empty data if the decoding process is not done).
        :type: list[int], int, list[int]
        """
        if self._decoder_state == State.SIZE_TAG.value:
            self._decoder_size_tag = byte

            self._decoder_state = self._decoder_state + 1

            return list(), 0, list()
        elif self._decoder_state == State.SIZE_TAG_2.value:
            self._decoder_size_tag = self._decoder_size_tag << 8
            self._decoder_size_tag = self._decoder_size_tag | byte
            self._decoder_state = self._decoder_state + 1

            return list(), 0, list()
        elif self._decoder_state == State.SIZE_TAG_3.value:
            self._decoder_size_tag = self._decoder_size_tag << 8
            self._decoder_size_tag = self._decoder_size_tag | byte

            for i in range(_PYNGHAM_SIZES):
                self._decoder_size_nr = i
                # If tag is intact, set known size
                size_tag = (_PYNGHAM_SIZE_TAGS[self._decoder_size_nr][0] << 16) | (_PYNGHAM_SIZE_TAGS[self._decoder_size_nr][1] << 8) | _PYNGHAM_SIZE_TAGS[self._decoder_size_nr][2]
                if self._tag_check(self._decoder_size_tag, size_tag):
                    self._decoder_state = State.SIZE_KNOWN.value
                    self._decoder_buf = []
                    break

            # If size tag is not found, every size can theoretically be attempted
            if self._decoder_state != State.SIZE_KNOWN.value:
                self._decoder_state = State.SIZE_TAG.value

                return list(), 0, list()

            return list(), 0, list()
        elif self._decoder_state == State.SIZE_KNOWN.value:
            # De-scramble
            self._decoder_buf.append(byte ^ _PYNGHAM_CCSDS_POLY[len(self._decoder_buf)])

            # Run Reed Solomon decoding, calculate packet length
            if len(self._decoder_buf) == _PYNGHAM_PL_PAR_SIZES[self._decoder_size_nr]:
                self._decoder_state = State.SIZE_TAG.value

                pl = list()
                errors = int()
                err_pos = list()

                pl, errors, err_pos = self._rsc[self._decoder_size_nr].decode(self._decoder_buf, [0], 0)

                pl = list(pl[1:])
                pl = pl[:_PYNGHAM_PL_SIZES[self._decoder_size_nr] - (self._decoder_buf[0] & _PYNGHAM_PADDING_BM)]

                # Check if the packet is decodeable and then if CRC is OK
                if Calculator(Configuration(16, 0x1021, 0xFFFF, 0xFFFF, True, True)).verify(bytes(self._decoder_buf[:len(pl)+1]), (self._decoder_buf[len(pl)+1] << 8) | self._decoder_buf[len(pl)+2]):
                    return pl, errors, err_pos
                else:
                    return list(), -1, list()

            return list(), 0, list()
