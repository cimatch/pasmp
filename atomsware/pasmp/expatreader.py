# -*- coding: utf-8 -*-
"""
Python API for Swift Message Processing for Python 2.0+
Created on 2019/12/09
@author: T.Shimada(Atomsware)
"""

from atomsware.pasmp import mtreader, mtutils


class _ClosedParser:
    def __init__(self):
        self.ErrorColumnNumber = None

    pass


class ExpatParser(mtreader.IncrementalParser, mtreader.Locator):

    def __init__(self, bufsize=2 ** 16 - 20):
        mtreader.IncrementalParser.__init__(self, bufsize)
        self._source = mtreader.InputSource()
        self._parser = None
        self.__col = 0
        self.__line = 1
        self.__systemid = None

    # MTReader methods

    def parse(self, source):
        source = mtutils.prepare_input_source(source)

        self._source = source
        try:
            mtreader.IncrementalParser.parse(self, source)
        except:
            self._close_source()
            raise

    def _close_source(self):
        source = self._source
        try:
            file = source.getCharacterStream()
            if file is not None:
                file.close()
        except:
            file = source.getByteStream()
            if file is not None:
                file.close()

    def close(self):
        if (self._parser is None or
                isinstance(self._parser, _ClosedParser)):
            return
        try:
            self._cont_handler.endDocument()
            self._parser = None
        finally:
            if self._parser is not None:
                parser = _ClosedParser()
                self._parser = parser
            self._close_source()

    def resetColumn(self):
        self.__col = 0

    def nextColumn(self):
        self.__col = self.__col + 1

    def getColumnNumber(self):
        return self.__col

    def resetLine(self):
        self.__line = 1

    def nextLine(self):
        self.resetColumn()
        self.__line = self.__line + 1

    def getLineNumber(self):
        return self.__line


def create_parser(*args, **kwargs):
    return ExpatParser(*args, **kwargs)
