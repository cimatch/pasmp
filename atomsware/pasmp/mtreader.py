# -*- coding: utf-8 -*-
"""
Python API for Swift Message Processing for Python 2.0+
Created on 2019/12/09
@author: T.Shimada(Atomsware)
"""
from atomsware.pasmp import handler
from ._exceptions import SwiftParseException, SwiftNotSupportedException
from collections import deque

class MTReader:

    def __init__(self):
        self._cont_handler = handler.ContentHandler()
        self._err_handler = handler.ErrorHandler()

    def parse(self, source):
        raise NotImplementedError("This method must be implemented!")

    def getContentHandler(self):
        return self._cont_handler

    def setContentHandler(self, handler):
        self._cont_handler = handler

    def getErrorHandler(self):
        return self._err_handler

    def setErrorHandler(self, handler):
        self._err_handler = handler

    def setLocale(self, locale):
        raise SwiftNotSupportedException("Locale support not implemented")


class IncrementalParser(MTReader):
    """ """

    def __init__(self, bufsize=2 ** 16):
        self._bufsize = bufsize
        self._locator = Locator()
        self._blockQueue = deque()
        self._currentBlock = None
        self._currentTag = None
        self._name = None
        self._block4 = False
        self._pos = 0
        MTReader.__init__(self)

    def parse(self, source):
        from . import mtutils
        source = mtutils.prepare_input_source(source)
        self._locator.resetLine()

        file = source.getCharacterStream()
        if file is None:
            file = source.getByteStream()

        buffer = file.read(self._bufsize)
        self.__analyze(buffer)
        while buffer:
            buffer = file.read(self._bufsize)
            self.__analyze(buffer)

        self.close()

    def __analyze(self, textMsg):
        """
        SWIFT MTメッセージの分析処理
            :param textMsg: MTメッセージ
            :return: void
        """
        if textMsg:
            self._pos = 0
            self._cont_handler.startDocument(self._locator)
        for x in textMsg:
            self._pos = self._pos + 1
            self._locator.nextColumn()
            if x == 45:  # "-"
                if self._locator.getColumnNumber() == 1 and textMsg[self._pos - 1] == 45 and textMsg[self._pos] == 125:
                    """ 先頭 -} タグ終了 & 4ブロック終了 """
                    self._cont_handler.endTag(self._locator, self._currentTag)
                    self._currentTag = None
                    self._block4 = False
                    self._pos = self._pos + 1
                else:
                    """データ"""
                    self._cont_handler.characters(self._locator, chr(x))
            elif x == 123:  # "{"
                if self._block4 is True and self._currentTag is not None:
                    """ブロック４内でタグ内の{はデータ"""
                    self._cont_handler.characters(self._locator, chr(x))
                else:
                    """ブロックかタグの開始"""
                    self._name = ""
            elif x == 58:  # ":"
                if self._locator.getColumnNumber() == 1:
                    if self._currentTag is not None:
                        """ 先頭コロンでタグ終了 """
                        self._cont_handler.endTag(self._locator, self._currentTag)
                        self._currentTag = None
                        self._name = ""
                elif len(self._name) == 1:
                    """ ブロックのコロン """
                    self._cont_handler.startBlock(self._locator, self._name)
                    if self._name == "4":
                        self._block4 = True
                    else:
                        self._block4 = False
                    self._currentBlock = self._name
                    self._blockQueue.append(self._name)
                    self._name = ""
                elif len(self._name) == 2 or len(self._name) == 3:
                    """ タグのコロン """
                    self._cont_handler.startTag(self._locator, self._name)
                    self._currentTag = self._name
                    self._name = ""
                else:
                    if self._currentTag is not None:
                        """ タグ内の値としてのコロン """
                        self._cont_handler.characters(self._locator, chr(x))
                    else:
                        """ 不明なコロン """
                        self._err_handler.error(SwiftParseException('Unknown colon', None, self._locator))
            elif x == 125:  # "}"
                if self._currentTag is not None:
                    """ }でタグ終了 """
                    self._cont_handler.endTag(self._locator, self._currentTag)
                    self._currentTag = None
                else:
                    """ }でブロック終了 """
                    self._cont_handler.endBlock(self._locator, self._blockQueue.pop())
                    self._currentBlock = None
            elif x == 10:  # "\r"
                if self._block4 is True:
                    """ブロック４内でタグ内の改行はデータ"""
                    self._cont_handler.characters(self._locator, chr(x))
                self._locator.nextLine()
            elif x == 13:  # "\n"
                if self._block4 is False:
                    """ 不明な改行 """
                    self._err_handler.error(SwiftParseException('Unknown line break', None, self._locator))
                if self._block4 is True:
                    """ブロック４内でタグ内の改行はデータ"""
                    self._cont_handler.characters(self._locator, chr(x))
            else:
                self._name = self._name + chr(x)
                if self._currentTag is not None or self._currentBlock is not None:
                    """ブロック内orタグ内はデータ"""
                    self._cont_handler.characters(self._locator, chr(x))
        if textMsg:
            self._cont_handler.endDocument()

    def close(self):
        raise NotImplementedError("This method must be implemented!")


class Locator:

    def __init__(self):
        self.__line = 1
        self.__col = 0

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

    def __str__(self):
        return '(' + str(self.__line) + ',' + str(self.__col) + ')'


class InputSource:

    def __init__(self, system_id=None):
        self.__system_id = system_id
        self.__public_id = None
        self.__encoding = "utf-8"
        self.__bytefile = None
        self.__charfile = None

    def setPublicId(self, public_id):
        self.__public_id = public_id

    def getPublicId(self):
        return self.__public_id

    def setSystemId(self, system_id):
        self.__system_id = system_id

    def getSystemId(self):
        return self.__system_id

    def setEncoding(self, encoding):
        self.__encoding = encoding

    def getEncoding(self):
        return self.__encoding

    def setByteStream(self, bytefile):
        self.__bytefile = bytefile

    def getByteStream(self):
        return self.__bytefile

    def setCharacterStream(self, charfile):
        self.__charfile = charfile

    def getCharacterStream(self):
        return self.__charfile


def _test():
    MTReader()
    IncrementalParser()
    Locator()


if __name__ == "__main__":
    _test()
