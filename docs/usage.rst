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

With the list of integers (*payload*) representing the data to encode into a packet. It is also possible to pass a byte array or an string containing the data to encode a packet:

.. code-block:: python

   pkt = x.encode(bytes([1, 2, 3]))

Or:

.. code-block:: python

   pkt = x.encode("test")

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

Serial Port Protocol (SPP)
==========================

To handle serial port packets, the procedure is very similar, as can be seen below:

1. Import the library:

.. code-block:: python

    import pyngham

Or import only the SPP class:

.. code-block:: python

    from pyngham import PyNGHamSPP

2. SPP initialization:

.. code-block:: python

    x = PyNGHamSPP()

3. To encode data, there is a command for each type of SPP packet. For example, a RX packet can be generated with the following command:

.. code-block:: python

    x.encode_rx_pkt(-50, -10, 4, 0, [0, 1, 2, 3, 4])

Generating a TX SPP packet:

.. code-block:: python

    x.encode_tx_pkt(0, [0, 1, 2, 3, 4])

Generating a command SPP packet:

.. code-block:: python

    x.encode_cmd_pkt([0, 1, 2, 3, 4])

Generating a local SPP packet:

.. code-block:: python

    x.encode_local_pkt(0, [0, 1, 2, 3, 4])

The encode commands will return a list with the byte sequence of the desired packet.

4. To decode an SPP packet, the following command can be used:

.. code-block:: python

    x.decode(pkt)

Or to decode byte by byte:

.. code-block:: python

    x.decode_byte(byte)

If successful, the decode command will return a dictionary with the decoded fields of the given packet.

The sequence below exemplifies all the presented methods above:

.. code-block:: python

    >>> from pyngham import PyNGHamSPP
    >>> x = PyNGHamSPP()
    >>> rx_pkt = x.encode_rx_pkt(-50, -10, 4, 0, [0, 1, 2, 3, 4])
    >>> print(rx_pkt)
    [36, 173, 98, 0, 13, 98, 73, 83, 25, 150, 190, 4, 0, 0, 1, 2, 3, 4]
    >>> x.decode(rx_pkt)
    {'type': 0, 'timestamp': 1648972569, 'noise_floor': -50, 'rssi': -10, 'symbol_errors': 4, 'flags': 0, 'payload': [0, 1, 2, 3, 4]}
    >>> tx_pkt = x.encode_tx_pkt(0, [0, 1, 2, 3, 4])
    >>> print(tx_pkt)
    [36, 159, 78, 1, 6, 0, 0, 1, 2, 3, 4]
    >>> x.decode(tx_pkt)
    {'type': 1, 'flags': 0, 'payload': [0, 1, 2, 3, 4]}
    >>> cmd_pkt = x.encode_cmd_pkt([0, 1, 2, 3, 4])
    >>> print(cmd_pkt)
    [36, 245, 214, 3, 5, 0, 1, 2, 3, 4]
    >>> x.decode(cmd_pkt)
    {'type': 3, 'payload': [0, 1, 2, 3, 4]}
    >>> local_pkt = x.encode_local_pkt(0, [0, 1, 2, 3, 4])
    >>> print(local_pkt)
    [36, 21, 158, 2, 6, 0, 0, 1, 2, 3, 4]
    >>> x.decode(local_pkt)
    {'type': 2, 'flags': 0, 'payload': [0, 1, 2, 3, 4]}

Extension Packets
=================

To handle extension packets, the procedure is also very similar, as can be seen below:

1. Import the library:

.. code-block:: python

    import pyngham

Or import only the SPP class:

.. code-block:: python

    from pyngham import PyNGHamExtension

2. Extension initialization:

.. code-block:: python

    x = PyNGHamExtension()

3. Before generating the extension packets, an empty list should be created. This list will be used to store the payload of the NGHam with the extensions.

.. code-block:: python

    pl = list()

4. For example, to generate an extension packet with the ID of the transmitter, the line below can be used:

.. code-block:: python

    pl = x.append_id_pkt(pl, x.encode_callsign("PU5GMA", 1), 1)

If successful, the generated extension packet will be stored in the *pl* variable. This can be used to encode a NGHam or SPP packet the same way as described before.

The same procedure can be used to append other extension packets to the same payload.

5. To decode an extension packet, the function below can be used:

.. code-block:: python

    res = x.decode(pl)

This way, the decoded extension packet will be stored in the *res* variable as a dictionaty with the content of the packet.

The sequence below exemplifies all the presented methods above:

.. code-block:: python

    >>> from pyngham import PyNGHamExtension
    >>> x = PyNGHamExtension()
    >>> pl = list()
    >>> pl = x.append_id_pkt(pl, x.encode_callsign("PU5GMA", 1), 1)
    >>> print(pl)
    [1, 9, 80, 85, 53, 71, 77, 65, 32, 1, 1]
    >>> x.decode(pl)
    [{'call_ssid': ('PU5GMA', 1), 'sequence': 1}]

.. note::
   Since the extension packets are not fully implemented and documented in the original NGHam implementation, the support for this resource is not complete yet. Some extension packet are already implemented and working, and some are not implemented because of lack of information about it. In the future, a definition of these packets are planned to be done.
