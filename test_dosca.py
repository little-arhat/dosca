#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import StringIO

import dosca

SIMPLE_TYPES = '''
kwd1 = and
kwd2 = [1, 2, 4]
kwd3 = "now something"
kwd4 = 'completely different'
kwd5 = 42
kwd6 = true
kwd7 =
'''

SECTIONS = '''
kwd1 = value1
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

class DoscaSuite(unittest.TestCase):
    def test_simple_types(self):
        source = StringIO.StringIO(SIMPLE_TYPES)
        result = {
            'kwd1': 'and',
            'kwd2': [1, 2, 4],
            'kwd3': 'now something',
            'kwd4': 'completely different',
            'kwd5': 42,
            'kwd6': True,
            'kwd7': None
            }
        self.assertEqual(dosca.parse(source), result)

    def test_sections(self):
        source = StringIO.StringIO(SECTIONS)
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
        source = StringIO.StringIO(COMMENTS)
        result = {
            'kwd1': 'value1',
            'section': {
                'kwd2': 'value2',
                'kwd3': 'value3'
            }
        }
        self.assertEqual(dosca.parse(source), result)

    def test_bad(self):
        bad_sources = map(StringIO.StringIO, [BAD1, BAD2, BAD3])
        for bad_source in bad_sources:
            self.assertRaises(dosca.ParseError,
                              dosca.parse,
                              bad_source)


if __name__ == '__main__':
    unittest.main()
