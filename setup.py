#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import dosca

setup(
    name='dosca',
    version=dosca.__version__,
    description='''Damn Simple Config File Parser.''',
    long_description=open('README.rst').read(),
    author=dosca.__author__,
    author_email='sokolov.r.v@gmail.com',
    url='https://github.com/little-arhat/dosca',
    packages=[
        'dosca'
    ],
    license='MIT',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2'
    ),
)
