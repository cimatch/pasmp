# -*- coding: utf-8 -*-
"""
Python API for Swift Message Processing for Python 2.0+
Created on 2019/12/09
@author: T.Shimada(Atomsware)
"""
from atomsware.pasmp.models import SwiftMessage, Block, Tag, create_block, create_tag


class ErrorHandler:

    def error(self, exception):
        raise exception

    def fatalError(self, exception):
        raise exception

    @staticmethod
    def warning(exception):
        print(exception)


class ContentHandler:

    def __init__(self):
        """ """

    def startDocument(self, locator):
        """ """

    def endDocument(self):
        """ """

    def startBlock(self, locator, blockNo):
        """ """

    def endBlock(self, locator, blockNo):
        """ """

    def startTag(self, locator, tagName):
        """ """

    def endTag(self, locator, tagName):
        """ """

    def characters(self, locator, content):
        """ """


class DomHandler(ContentHandler):

    def __init__(self):
        self.mt = None
        self.blockLevel = 0
        self.currentBlock = None
        self.currentTag = None
        self.value = ""
        ContentHandler.__init__(self)

    def startDocument(self, locator):
        self.mt = SwiftMessage()

    def startBlock(self, locator, blockNo):
        self.value = ""
        self.blockLevel += 1
#        print(blockNo + ' Start')
        if self.blockLevel == 1:
            block = create_block(blockNo, self.mt)
            self.mt.blocks.append(block)
        else:
            block = create_block(blockNo, self.currentBlock)
            self.currentBlock.blocks.append(block)
        block.block_no = blockNo
        self.currentBlock = block

    def startTag(self, locator, tagName):
        self.value = ""
        tag = create_tag(tagName, self.currentBlock)
        self.currentBlock.tags.append(tag)
        self.currentTag = tag

    def endTag(self, locator, tagName):
        self.currentTag.setTagText(self.value.strip())
        self.value = ""

    def endBlock(self, locator, blockNo):
        self.currentBlock.setBlockText(self.value)
        self.blockLevel -= 1
 #       print(blockNo + ' End')
        if self.blockLevel == 0:
            self.currentBlock = None
        else:
            self.currentBlock = self.currentBlock.parent

    def endDocument(self):
        """"""

    def characters(self, locator, ch):
        self.value = self.value + ch
