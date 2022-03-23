********
Overview
********

The PyNGHam library is a Python version of the original NGHam protocol library written in C by Jon Petter Skagmo (LA3JPA) [1]_.

The NGHam protocol is a link protocol partly inspired by AX.25 [2]_, with the idea to be used in ham radio packet communication. It was developed in the context of a CubeSat development in the Norwegian University of Science and Technology (NTNU) [3]_, and is being used in a few CubeSat missions since then.

A list of known satellites that used or plan to use the NGHam protocol are presented below:

* **FloripaSat-1** [4]_
* **GOLDS-UFSC (a.k.a. FloripaSat-2)** [5]_
* **Catarina-A1**
* **PION-BR1** [6]_
* **Aldebaran-1**
* **NUTS-1** [7]_

The top three satellites of the list above, are satellites developed (or in development) by the same research group: the *Space Technology Research Laboratory* (SpaceLab) [8]_, from *Universidade Federal de Santa Catarina* (Brazil), which was the context where this library was developed. As can be seen from the list, the NGHam is becoming a very popular protocol in Brazilian CubeSats :)

The objective of this library is to offer an alternative purely written Python for the original NGHam library. This way, this can be used in simulations, packet decoding and encoding software, telecommunication classes, and so far.

References
==========

.. [1] https://github.com/skagmo/ngham
.. [2] http://www.ax25.net/
.. [3] Løfaldli, André; Birkeland, Roger. *Implementation of a Software Defined Radio Prototype Ground Station for CubeSats*. The 4S Symposium 2016.
.. [4] Marcelino, Gabriel M.; Martinez, Sara V.; Seman, Laio O., Slongo, Leonardo K.; Bezerra, Eduardo A. *A Critical Embedded System Challenge: The FloripaSat-1 Mission*. IEEE Latin America Transactions, Vol. 18, Issue 2, 2020.
.. [5] https://github.com/spacelab-ufsc/floripasat2-doc
.. [6] https://github.com/pion-labs/PION-BR1/wiki/Radio-Information
.. [7] Løfaldli, André; Birkeland, Roger. *Implementation of a Software Defined Radio Prototype Ground Station for CubeSats*. The 4S Symposium 2016.
.. [8] https://spacelab.ufsc.br/
