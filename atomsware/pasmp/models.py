# -*- coding: utf-8 -*-
"""
Python API for Swift Message Processing for Python 2.0+
Created on 2019/12/09
@author: T.Shimada(Atomsware)
"""


class SwiftMessage:
    def __init__(self):
        self.name = ""
        self.acknowledgement = False
        self.retrieved = False
        self.blocks = list()

    def __str__(self):
        val = self.name + ' '
        for block in self.blocks:
            val = val + str(block) + ' '
        return val

    class Meta:
        verbose_name = 'SWIFT Message'
        verbose_name_plural = 'SWIFT Message'


class Block:
    def __init__(self, block_no, parent):
        self.parent = parent
        self.block_no = block_no
        self.block_text = ''
        self.tags = list()

    def setBlockText(self, block_text):
        self.block_text = block_text

    def __str__(self):
        val = '[' + self.block_no + ':' + self.block_text + ' '
        for tag in self.tags:
            val = val + str(tag) + ' '
        return val + ']'

    class Meta:
        verbose_name = 'Block'
        verbose_name_plural = 'Block'


class BasicHeaderBlock(Block):

    def __init__(self, block_no, parent):
        self.appID = ''
        self.serviceID = ''
        self.lTAddr = ''
        self.sessionID = ''
        self.sequenceID = ''
        super(BasicHeaderBlock, self).__init__(block_no, parent)

    def setBlockText(self, block_text):
        super(BasicHeaderBlock, self).setBlockText(block_text)
        self.appID = block_text[0:1]
        self.serviceID = block_text[1:3]
        if self.serviceID == '21':
            self.parent.acknowledgement = True
        self.lTAddr = block_text[3:15]
        self.sessionID = block_text[15:19]
        self.sequenceID = block_text[19:25]


class ApplicationHeaderBlock(Block):

    def __init__(self, block_no, parent):
        self.ioType = ''
        self.messageType = ''
        self.lTAddr = ''
        self.priority = ''
        self.deliveryMonitorField = ''
        self.obsolescencePeriod = ''
        self.inputTime = ''
        self.messageInputReference = ''
        self.outputDate = ''
        self.outputTime = ''
        super(ApplicationHeaderBlock, self).__init__(block_no, parent)

    def setBlockText(self, block_text):
        super(ApplicationHeaderBlock, self).setBlockText(block_text)
        self.ioType = block_text[0:1]
        self.messageType = block_text[1:4]
        self.parent.name = 'MT' + self.messageType
        if self.messageType == '021':
            self.parent.retrieved = True
        if self.ioType == 'I':
            self.lTAddr = block_text[4:16]
            self.priority = block_text[16:17]
            self.deliveryMonitorField = block_text[17:18]
            self.obsolescencePeriod = block_text[18:21]
        if self.ioType == 'O':
            self.inputTime = block_text[4:8]
            self.messageInputReference = block_text[8:36]
            self.outputDate = block_text[36:42]
            self.outputTime = block_text[42:46]
            self.priority = block_text[46:47]


class UserHeaderBlock(Block):
    """ """


class TextBlock(Block):

    def __str__(self):
        val = '[' + self.block_no + ':' + self.block_text + ' ' + '\r\n'
        for tag in self.tags:
            val = val + str(tag) + ' ' + '\r\n'
        return val + ']'


class AckTextBlock(TextBlock):
    """ """


class HistoryBlock(TextBlock):

    def __init__(self, block_no, parent):
        self.retrieved = False
        self.acknowledgement = False
        self.blocks = list()
        super(HistoryBlock, self).__init__(block_no, parent)

    def __str__(self):
        val = '[' + self.block_no + ':' + self.block_text + ' '
        for tag in self.tags:
            val = val + str(tag) + ' '
        for block in self.blocks:
            val = val + str(block) + ' '
        return val + ']'


class TrailerBlock(Block):
    """ """


class Tag:
    def __init__(self, tagName, parent):
        self.parent = parent
        self.block = None
        self.tag_no = ''
        self.tag_option = ''
        self.tag_text = ''
        self.setTagName(tagName)

    def setTagName(self, tagName):
        self.tag_no = tagName[0:2]
        if len(tagName) >= 3:
            self.tag_option = tagName[2:]

    def setTagText(self, tag_text):
        self.tag_text = tag_text

    def __str__(self):
        return '(' + self.tag_no + self.tag_option + ':' + self.tag_text + ')'

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tag'


class UnkownTag(Tag):
    """ """


blocks_map = {
    "1": "atomsware.pasmp.models,BasicHeaderBlock",
    "2": "atomsware.pasmp.models,ApplicationHeaderBlock",
    "3": "atomsware.pasmp.models,UserHeaderBlock",
    "4": "atomsware.pasmp.models,TextBlock",
    "4R": "atomsware.pasmp.models,HistoryBlock",
    "4A": "atomsware.pasmp.models,AckTextBlock",
    "5": "atomsware.pasmp.models,TrailerBlock",
    "S": "atomsware.pasmp.models,Block",
}


def create_block(block_no, parent):
    try:
        if block_no == '4' and parent.retrieved:
            key = block_no + 'R'
        elif block_no == '4' and parent.acknowledgement:
            key = block_no + 'A'
        else:
            key = block_no
        cls_def = blocks_map[key]
        clz = cls_def.split(',')
        mod = __import__(clz[0], fromlist=[clz[1]])
        clazz = getattr(mod, clz[1])
        block = clazz(block_no, parent)
        return block
    except:
        print('Unkown ' + block_no)
        return Block(block_no, parent)


tags_map = {
    "20": "atomsware.pasmp.models,Tag",
}


def create_tag(tag_name, parent):
    try:
        cls_def = tags_map[tag_name]
        clz = cls_def.split(',')
        mod = __import__(clz[0], fromlist=[clz[1]])
        clazz = getattr(mod, clz[1])
        tag = clazz(tag_name, parent)
        return tag
    except:
        #print('Unkown ' + tag_name)
        return UnkownTag(tag_name, parent)
