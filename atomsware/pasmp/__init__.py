# -*- coding: utf-8 -*-
"""
Python API for Swift Message Processing for Python 2.0+
Created on 2019/12/09
@author: T.Shimada(Atomsware)
"""

import atomsware.pasmp.expatreader
from ._exceptions import SwiftException, SwiftNotRecognizedException, \
    SwiftParseException, SwiftNotSupportedException, \
    SwiftReaderNotAvailable
from .handler import ContentHandler, ErrorHandler

__copyright__    = 'Copyright (C) 2019 Atomsware'
version = "0.4.0"

default_parser_list = ["atomsware.pasmp.expatreader"]


def make_parser(parser_list=[]):
    for parser_name in parser_list + default_parser_list:
        try:
            return _create_parser(parser_name)
        except ImportError:
            import sys
            if parser_name in sys.modules:
                raise
        except SwiftReaderNotAvailable:
            pass

    raise SwiftReaderNotAvailable("No parsers found", None)


def _create_parser(parser_name):
    drv_module = __import__(parser_name, fromlist=['create_parser'])
    return drv_module.create_parser()
