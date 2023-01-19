#!/usr/bin/end python

#
# setup.py
# 
# Copyright (C) 2023, Gabriel Mariano Marcelino - PU5GMA <gabriel.mm8@gmail.com>
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


import setuptools
import os

exec(open('pyngham/version.py').read())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name                            = "pyngham",
    version                         = __version__,
    author                          = "Gabriel Mariano Marcelino - PU5GMA",
    author_email                    = "gabriel.mm8@gmail.com",
    maintainer                      = "Gabriel Mariano Marcelino - PU5GMA",
    maintainer_email                = "gabriel.mm8@gmail.com",
    url                             = "https://github.com/mgm8/pyngham",
    license                         = "LGPLv3",
    description                     = "PyNGHam library",
    long_description                = long_description,
    long_description_content_type   = "text/markdown",
    platforms                       = ["Linux", "Windows", "Solaris", "Mac OS-X", "Unix"],
    classifiers                     = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Ham Radio",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
    download_url                    = "https://github.com/mgm8/pyngham/releases",
    packages                        = setuptools.find_packages(),
    install_requires                = ['crc==3.0.0'],
)
