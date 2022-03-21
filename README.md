# PyNGHam

<a href="https://pypi.org/project/pyngham/">
    <img src="https://img.shields.io/pypi/v/pyngham?style=for-the-badge">
</a>
<a href="https://pypi.org/project/pyngham/">
    <img src="https://img.shields.io/pypi/pyversions/pyngham?style=for-the-badge">
</a>
<a href="https://github.com/mgm8/pyngham/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/mgm8/pyngham?style=for-the-badge">
</a>
<a href="https://github.com/mgm8/pyngham/actions">
    <img src="https://img.shields.io/github/workflow/status/mgm8/pyngham/Test?style=for-the-badge">
</a>

## Overview

The PyNGHam library is a Python version of the original NGHam protocol library written in C by Jon Petter Skagmo (LA3JPA).

The original implementation and a further description of the protocol can be found [here](https://github.com/skagmo/ngham).

## Dependencies

* [crc](https://pypi.org/project/crc/)

## Installing

* ```pip3 install pyngham```

Or, from the source files:

* ```python setup.py install```

## Documentation

The documentation page is available [here](https://mgm8.github.io/pyngham/). Instructions to build the documentation page are described below.

### Dependencies

* sphinx-rtd-theme

### Building the Documentation

* ```python setup.py build_sphinx```

## Usage Example

The usage of the library is pretty straightforward, after the initialization, there are two methods: one to encode a list of bytes, and other to decode a packet. Below there is a basic usage example:

```
from pyngham import PyNGHam

data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

pkt = PyNGHam().encode(data)

pl, errors = PyNGHam().decode(pkt)

print(pl)
```

## License

This project is licensed under LGPLv3 license.
