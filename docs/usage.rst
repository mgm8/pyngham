*****
Usage
*****

The usage of the library is very straightforward. Basically, four steps are required to perform the encode and decode sequence.

1. Import the library:

.. code-block:: python

    import pyngham

Or import only the main class:

.. code-block:: python

    from pyngham import PyNGHam

2. Library initialization:

.. code-block:: python

    x = PyNGHam()

3. To encode data into a NGHam packet, the following command can be used:

.. code-block:: python

    pkt = x.encode(payload)

With the list of integers (*payload*) representing the data to encode into a packet.

4. To decode a packet, the following command can be used:

.. code-block:: python

    x.decode(pkt)

This command will return three outputs:

1. The decoded data as a list of integers, representing the bytes of the original message
2. The number of identified errors (malformed bits)
3. The localization of the error bits (a list with the positions)

This example is fully presented below:

.. code-block:: python

    from pyngham import PyNGHam

    x = PyNGHam()

    pkt = x.encode([0, 1, 2, 3, 4])

    x.decode(pkt)

Output of the example above:

.. code-block:: python

    >>> from pyngham import PyNGHam
    >>> x = PyNGHam()
    >>> pkt = x.encode([0, 1, 2, 3, 4])
    >>> x.decode(pkt)
    ([0, 1, 2, 3, 4], 1, [207])
