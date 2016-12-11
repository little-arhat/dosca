#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import unittest

import dosca

SIMPLE_TYPES = '''
kwd1 = and
kwd2 = [1, 2, 4]
kwd3 = "now something"
kwd4 = 'completely different'
kwd5 = 42
kwd6 = true
kwd7 =
kwd8 = []
kwd9 = ['123,45', '67,8','68']
'''

SECTIONS = '''kwd1 = value1
[section1]
kwd2 = value2
[section2]
kwd3 = value3
[[section3]]
kwd4 = value4
[[section4]]
kwd5 = value5
[section5]
kwd6 = value6
'''

COMMENTS = '''
# comment
kwd1 =   value1
# comment
[ section ]
kwd2 = value2
kwd3 = value3
'''

BAD1 = '''
kwd1 = value
[section]]
'''

BAD2 = '''
[section]
kwd1 = value1
[[[section]]]
kwd2 = value2
'''

BAD3 = '''
kwd1 = value1
some garbage
'''

CUSTOM_PARSERS = '''
kwd1 = yes
kwd2 = no
kwd3 = on
kwd4 = off
kwd5 = simplestring
'''

ARRAY_KEYS = '''
kwd[] = 1
kwd[] = 2
kwd[] = 3
[section]
k[] = 1
k[] = 2
'''

class DoscaSuite(unittest.TestCase):
    def test_simple_types(self):
        source = SIMPLE_TYPES.split('\n')
        result = {
            'kwd1': 'and',
            'kwd2': [1, 2, 4],
            'kwd3': 'now something',
            'kwd4': 'completely different',
            'kwd5': 42,
            'kwd6': True,
            'kwd7': None,
            'kwd8': [],
            'kwd9': ['123,45', '67,8', '68']
            }
        self.assertEqual(dosca.parse(source), result)

    def test_sections(self):
        source = SECTIONS.split('\n')
        result = {
            'kwd1': 'value1',
            'section1': {
                'kwd2': 'value2',
            },
            'section2': {
                'kwd3': 'value3',
                'section3': {
                    'kwd4': 'value4'
                    },
                'section4': {
                    'kwd5': 'value5'
                }
            },
            'section5': {
                'kwd6': 'value6'
                }
        }
        self.assertEqual(dosca.parse(source), result)

    def test_comments_and_spaces(self):
        source = COMMENTS.split('\n')
        result = {
            'kwd1': 'value1',
            'section': {
                'kwd2': 'value2',
                'kwd3': 'value3'
            }
        }
        self.assertEqual(dosca.parse(source), result)

    def test_bad(self):
        bad_sources = map(lambda s: s.split('\n'), [BAD1, BAD2, BAD3])
        for bad_source in bad_sources:
            self.assertRaises(dosca.ParseError,
                              dosca.parse,
                              bad_source)

    def test_custom_parsers(self):
        source = StringIO(CUSTOM_PARSERS)
        result = {
            'kwd1': True,
            'kwd2': False,
            'kwd3': True,
            'kwd4': False,
            'kwd5': 'simplestring'
        }
        custom_parsers = [
            (lambda x: x.lower() == 'yes', lambda _: True),
            (lambda x: x.lower() == 'on', lambda _: True),
            (lambda x: x.lower() == 'no' or x.lower() == 'off',
             lambda _: False)
        ]
        self.assertEqual(dosca.parse(source, custom_parsers=custom_parsers),
                         result)

    def test_array_keys(self):
        source = ARRAY_KEYS.split('\n')
        result = {
            'kwd[]': [1,2,3],
            'section': {
                'k[]': [1, 2]
            }
        }
        self.assertEqual(dosca.parse(source,
                                     key_hooks=[dosca.ext.PHP_ARRAYS]),
                         result)

    def test_extensions(self):
        source = StringIO(CUSTOM_PARSERS)
        result = {
            'kwd1': True,
            'kwd2': False,
            'kwd3': True,
            'kwd4': False,
            'kwd5': 'simplestring'
        }
        parse = dosca.ext.make_parse(dosca.ext.YES_NO_BOOL,
                                     dosca.ext.ON_OFF_BOOL)
        self.assertEqual(dict(parse(source)), result)

    def test_save(self):
        source = filter(None, SECTIONS.split('\n'))
        parsed = dosca.parse(source)
        sink = StringIO()

        dosca.save(parsed, sink)

        sink.seek(0)
        saved = sink.read()
        self.assertEqual(SECTIONS, saved)


if __name__ == '__main__':
    unittest.main()
