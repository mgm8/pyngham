#
# test.py
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


from pyngham import PyNGHam
from random import randrange

def main(args):
    print("Testing the PyNGHam library...", end='')

    pngh = PyNGHam()

    for i in range(1, 220+1):
        # Generating random packet payload
        pl = list()
        for j in range(i):
            pl.append(randrange(256))

        # Encoding the packet
        pkt = pngh.encode(pl)

        # Maximum allowed number of errors
        num_err = int()
        if (i < (159 + 8 + 3)):
            num_err = int(16/2) - 1
        else:
            num_err = int(32/2) - 1

        # Randomly adding error bits
        for j in range(num_err):
            err_byte = randrange(8 + 3, 8 + 3 + i)
            err_bit = randrange(8)
            byte_with_err = 1 << err_bit
            pkt[err_byte] = pkt[err_byte] ^ byte_with_err

        # Trying to decode the packet with errors
        dec_pl, errors, err_loc = pngh.decode(pkt)

        if (pl != dec_pl):
            print("FAILURE!")
            print("Error encoding/decoding a packet!")

            return -1

    print("SUCCESS!")

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
