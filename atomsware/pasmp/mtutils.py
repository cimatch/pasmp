# -*- coding: utf-8 -*-
"""
Python API for Swift Message Processing for Python 2.0+
Created on 2019/12/09
@author: T.Shimada(Atomsware)
"""
import os
import urllib

from . import mtreader


def prepare_input_source(source, base=""):
    """This function takes an InputSource and an optional base URL and
    returns a fully resolved InputSource object ready for reading."""

    if isinstance(source, str):
        source = mtreader.InputSource(source)
    elif hasattr(source, "read"):
        f = source
        source = mtreader.InputSource()
        if isinstance(f.read(0), str):
            source.setCharacterStream(f)
        else:
            source.setByteStream(f)
        if hasattr(f, "name") and isinstance(f.name, str):
            source.setSystemId(f.name)

    if source.getCharacterStream() is None and source.getByteStream() is None:
        sysid = source.getSystemId()
        basehead = os.path.dirname(os.path.normpath(base))
        sysidfilename = os.path.join(basehead, sysid)
        if os.path.isfile(sysidfilename):
            source.setSystemId(sysidfilename)
            f = open(sysidfilename, "rb")
        else:
            source.setSystemId(urllib.parse.urljoin(base, sysid))
            f = urllib.request.urlopen(source.getSystemId())

        source.setByteStream(f)

    return source
