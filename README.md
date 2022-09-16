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

This library is available in the PyPI repository, and can be installed with the following command:

* ```pip install pyngham```

Or, directly from the source files:

* ```python setup.py install```

## Documentation

The documentation page is available [here](https://mgm8.github.io/pyngham/). Instructions to build the documentation page are described below.

### Dependencies

* [Sphinx](https://pypi.org/project/Sphinx/)
* [sphinx-rtd-theme](https://pypi.org/project/sphinx-rtd-theme/)

### Building the Documentation

The documentation pages can be built with Sphinx by running the following command inside the ``docs`` folder:

* ```make html```

## Usage Example

The usage of the library is pretty straightforward, after the initialization, there are two methods: one to encode a list of bytes, and other to decode a packet. Below there is a basic usage example:

```python
from pyngham import PyNGHam

pngh = PyNGHam()

data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

pkt = pngh.encode(data)

print("Encoded packet:", pkt)

pl, errors, errors_pos = pngh.decode(pkt)

print("Decoded data:", pl)
print("Number of errors:", errors)
print("Errors positions:", errors_pos)
```

More usage examples can be found in the documentation [page](https://mgm8.github.io/pyngham/).

## License

This project is licensed under LGPLv3 license.
