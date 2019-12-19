# -*- coding: utf-8 -*-
"""
Python API for Swift Message Processing for Python 2.0+
Created on 2019/12/09
@author: T.Shimada(Atomsware)
"""


class SwiftException(Exception):

    def __init__(self, msg, exception=None):
        self._msg = msg
        self._exception = exception
        Exception.__init__(self, msg)

    def getMessage(self):
        return self._msg

    def getException(self):
        return self._exception

    def __str__(self):
        return self._msg

    def __getitem__(self, ix):
        raise AttributeError("__getitem__")


class SwiftParseException(SwiftException):

    def __init__(self, msg, exception, locator):
        SwiftException.__init__(self, msg, exception)
        self._locator = locator

        self._systemId = self._locator.getSystemId()
        self._colnum = self._locator.getColumnNumber()
        self._linenum = self._locator.getLineNumber()

    def getColumnNumber(self):
        return self._colnum

    def getLineNumber(self):
        return self._linenum

    def getPublicId(self):
        return self._locator.getPublicId()

    def getSystemId(self):
        return self._systemId

    def __str__(self):
        sysid = self.getSystemId()
        if sysid is None:
            sysid = "<unknown>"
        linenum = self.getLineNumber()
        if linenum is None:
            linenum = "?"
        colnum = self.getColumnNumber()
        if colnum is None:
            colnum = "?"
        return "%s:%s:%s: %s" % (sysid, linenum, colnum, self._msg)


class SwiftNotRecognizedException(SwiftException):
    """ """


class SwiftNotSupportedException(SwiftException):
    """ """


class SwiftReaderNotAvailable(SwiftNotSupportedException):
    """ """
