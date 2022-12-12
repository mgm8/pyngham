****************************************
Development Instructions and Information
****************************************

Automated Tests
===============

The project contains some automated tests for improve the correctness and the confiability of the source code, by testing key functional aspects of the code.

All tests are presented in the "tests" folder, and are divided in three parts:

* **Extension tests**: The extension tests contains tests for encoding and decoding most part of the extension packets. The packets are encoded and decoded using random data.
* **RF tests**: The RF tests contains the main test of the library. This test ensure the proper functioning of the encoding and decoding of NGHam packets, by generating packets with random data and with all possible quantity of bytes (1 to 220).
* **SPP tests**: The Serial Port Protocol tests (SPP) tests the encoding and decoding of SPP packets, similarly to the RF tests.

The tests are executed using the PyTests tool [1]_ and are integrated into the GitHub repository, using GitHub Actions. This way, at every new commit or merge to the main branch, the tests are performed automatically.

Together with the code tests, the documentation is also built and deployed automatically when a merge to the main branch is made.

Packaging the Project
=====================

This page presents the instructions to packaging the source files of the project.

Generating a RPM Package
------------------------

To generate an RPM package, execute the command below:

::

    python setup.py bdist_rpm


If successful, the generated RPM package will be available in *dist/*.

References
==========

.. [1] https://pytest.org/
