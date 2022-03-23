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
2. The number of identified errors (malformed bytes)
3. The localization of the bytes with errors (a list with the positions)

There is also a method do decode a packet byte by byte. This is useful for decoding packets being received in a stream of bits or bytes.

.. code-block:: python

   x.decode_byte(pkt[i])

With this method, the output will be the same as the usual *decode* function, but with an empty decoded data list when the packet is not ready yet (not fully decoded).

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
    ([0, 1, 2, 3, 4], 0, [])

A more complete example with an error correction demonstration is presented below:

.. code-block:: python

    >>> from pyngham import PyNGHam
    >>> x = PyNGHam()
    >>> pkt = x.encode([0, 1, 2, 3, 4])
    >>> pkt[30] = 5
    >>> x.decode(pkt)
    ([0, 1, 2, 3, 4], 1, [227])

As can be seen from the final output, one error was detected on position 227, and the original message was fully restored.
