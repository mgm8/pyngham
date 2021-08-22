#
# test.py
# 
# Copyright (C) 2021, Gabriel Mariano Marcelino - PU5GMA <gabriel.mm8@gmail.com>
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
        pl = list()
        for j in range(i):
            pl.append(randrange(256))
    
        pkt = pngh.encode(pl)

        dec_pl, errors = pngh.decode(pkt)
    
        if (pl != dec_pl):
            print("FAILURE!")
            print("Error encoding/decoding a packet!")

            return -1

    print("SUCCESS!")

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
