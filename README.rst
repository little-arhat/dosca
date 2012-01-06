Dosca -- Damn Simple Config Parser
==================================

About
-----

Just parses ini-style file and return dict with values. Really simple.

Features
--------

- Knows str, int, list, boolean and None types
- Supports sections and subsections
- Supports custom converters
- Easy to use -- one function!

API
---

``parse`` function takes any iterable (fileobj, for example), which produces strings and returns filled ``dict`` or raises ``ParseError``.

``parse_file`` helper function takes path to file, opens it and passes fileobj to ``parse`` functino.

FAQ
---

Q1: Does 'dosca' have validation capabilities?

A1: No, it's not. If you want validate your config, use library designed for this task.
`Contract <https://github.com/barbuza/contract>`_, `Procrustes <https://github.com/Deepwalker/procrustes>`_ or, perhaps, `Damn Simple Validation Library <https://github.com/little-arhat/kuvalda>`_?



Q2: Does it support interpolation or some complex types?

A2: No, it's not. When I say 'simple', I mean really simple. Dosca only support basic things, essential for parsing config files.
If you want advanced features, use `ConfigObj <http://www.voidspace.org.uk/python/configobj.html>`_ or `ConfigParser <http://docs.python.org/library/configparser.html>`_. Or xml and dtd?

Q3: How to use this library?
A3: Just pass fileobj to dosca.parse or see test_dosca.py for details.

Install
-------

~/yourvirtualenv/python setup.py install

pip install dosca

License
-------

The MIT License, in LICENSE file.
