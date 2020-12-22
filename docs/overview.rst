********
Overview
********

`RAMSTK` provides several analytical tools for estimating the RAMS metrics for
electromechanical systems.

Requirements
============

Currently RAMSTK supports Python 3.7+ and requires the following Python
packages to be installed somewhere in your PYTHONPATH.

.. literalinclude:: ../requirements.in

If you're planning to help develop RAMSTK, the following Python packages will
need to be installed. It is recommended you use a virtual environment for
development, but you could install these in a user or system location if you
choose.

.. literalinclude:: ../requirements-test.in

In order to build this documentation, you will need to install the following
Python packages.

.. literalinclude:: ../requirements-dev.in

If you're building the documentation to host locally, you are free to use
whatever Sphinx theme you'd like.  I happen to prefer the
`py3doc enhanced theme <https://github.com/ionelmc/sphinx-py3doc-enhanced-theme>`_.

Installation
============

`RAMSTK` can be installed in several ways.  Firstly, `RAMSTK` is available from
PyPi.

.. code-block:: bash

    pip install ramstk

Or the source code can be checked-out from GitHub and installed the
old-fashioned way.

.. code-block:: bash

    git checkout https://github.com/ReliaQualAssociates/ramstk.git ramstk.git
    cd ramstk.git
    python setup.py install --user

where the *--user* switch is optional if you're sure you want to install
`RAMSTK` in a system-wide location.

License
=======

`RAMSTK` is provided to you under the BSD, 3-clause license, reproduced below.

.. literalinclude:: ../LICENSE
