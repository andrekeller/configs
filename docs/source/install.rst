============
Installation
============

.. _`install`:

confi.gs is a pretty straight-forward Django application, so every generic
installation guide should work.

For some project dependencies, external libraries are needed in order to compile
them.

Currently this is at least:

* libpq (psycopg2)
* libyaml (pyyaml)
* pcre (uwsgi)
* openssl (uwsgi)

confi.gs also depends on postgresql 9.4 or later, as previous versions do not
have support for inet\_ops GiST indexes. All other database backends supported
by Django will not work for confi.gs


Installation methods
====================

.. _`install_methods`:

.. toctree::
    :maxdepth: 2

    _install/compose
    _install/manual
