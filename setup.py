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
    description='''Dumb Simple Config File Parser.''',
    long_description=open('README.rst').read(),
    author='Roma Sokolov',
    author_email='sokolov.r.v@gmail.com',
    url='https://github.com/little_arhat/dosca',
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
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)
