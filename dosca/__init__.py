# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .dosca import parse, parse_file, ParseError, save, save_file
from . import ext


__all__ = ('parse', 'parse_file', 'ParseError', 'ext', 'save', 'save_file')


__version__ = '1.4'
__author__ = 'Roma Sokolov'
__license__ = 'MIT'
