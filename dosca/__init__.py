# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .dosca import parse, parse_file, ParseError, save, save_file, dump
from . import ext


__all__ = ('parse', 'parse_file', 'ParseError',
           'ext',
           'save', 'save_file', 'dump')


__version__ = '2.0.0'
__author__ = 'Roma Sokolov'
__license__ = 'MIT'
