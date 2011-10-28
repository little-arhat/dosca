Dosca -- Dumb Simple Config Parser
========

About
-----

Just parses ini-style file and return dict with values. Really dumb.

Features
--------

- Knows str, int, list, boolean and None types
- Supports sections and subsections
- Easy to use -- one function!

FAQ
---

Q1: Does 'dosca' have validation capabilities?
A1: No, it's not. If you want validate your config, use library designed for this task. Construct, Procrustes or, perhaps, Dumb Validation?


Q2: Does it support interpolation or some complex types?
A2: No, it's not. When I say 'dumb', I mean really dumb. Dosca only support basic features, essential for parsing config files.
If you want advanced features, use ConfigObj or ConfigParser. Or xml and dtd?

Install
-------

~/yourvirtualenv/python setup.py install

Cheesshop package coming soon.

License
-------

The MIT License, in LICENSE file.
