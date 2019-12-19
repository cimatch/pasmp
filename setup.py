#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

try:
    with open('README.rst') as f:
        readme = f.read()
except IOError:
    readme = ''


def _requires_from_file(filename):
    return open(filename).read().splitlines()


# version
here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '')
                for line in open(os.path.join(here,
                                              'atomsware/pasmp',
                                              '__init__.py'))
                if line.startswith('__version__ = ')),
               '0.0.dev0')

setup(
    name="pasmp",
    version='0.3.1',
    url='https://github.com/cimatch/pasmp',
    author='atomsware',
    author_email='shimada@atomsware.co.jp',
    maintainer='atomsware',
    maintainer_email='shimada@atomsware.co.jp',
    description='Python API for Swift Message Processing',
    #data_files=[('', ['README.rst', 'CHANGES.rst'])],
    #long_description='%s\n\n%s' % (open('README.rst', encoding='utf8').read(),
    #                               open('CHANGES.rst', encoding='utf8').read()),
    long_description=' Python API for Swift Message Processing (PASMP) is an API for handling Swift messages like SAX and DOM, \
                        handling XML in Python. It is intended to make it easy to develop a system that handles SWIFT messages \
                        by making it open source.',
    packages=find_packages(),
    install_requires=[],
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points="""
    """,
)
