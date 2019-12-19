PASMP
=====

Swift messages in Python
"Python API for Swift Message Processing" (PASMP) is an API for handling Swift messages like SAX and DOM,
handling XML in Python. It is intended to make it easy to develop a system that handles SWIFT messages
by making it open source.

INSTALLATION
==============

::

 $ pip install pasmp


USAGE pattern1
==============

.. code:: python

    import atomsware.pasmp
    from atomsware.pasmp.handler import *


    class QuotationHandler(ContentHandler):
        value = ""

        def __init__(self):
            ContentHandler.__init__(self)

        def startDocument(self, locator):
            print('=== Begin Document ===' + str(locator))

        def startBlock(self, locator, blockNo):
            print('## Begin Block' + blockNo + ' ---' + str(locator))
            self.value = ""

        def startTag(self, locator, tagName):
            print('--- Begin Tag' + tagName + ' ---' + str(locator))
            self.value = ""

        def endTag(self, locator, tagName):
            print(self.value.strip())
            print('--- End Tag' + tagName + ' ---' + str(locator))

        def endBlock(self, locator, blockNo):
            if blockNo == "1" or blockNo == "2":
                print(self.value)
            print('## End Block' + blockNo + ' ---' + str(locator))

        def endDocument(self):
            print('=== End Document ===')

        def characters(self, locator, ch):
            self.value = self.value + ch


    if __name__ == '__main__':
        parser = atomsware.pasmp.make_parser()
        handler = QuotationHandler()
        parser.setContentHandler(handler)
        parser.parse("sample1.mt")


USAGE pattern2
==============

.. code:: python

    import atomsware.pasmp
    from atomsware.pasmp.handler import *
    from atomsware.pasmp.models import *

    if __name__ == '__main__':
        parser = atomsware.pasmp.make_parser()
        handler = DomHandler()
        parser.setContentHandler(handler)
        parser.parse("sample2.mt")
        dom = handler.mt

        for block in dom.blocks:
            if isinstance(block, BasicHeaderBlock):
                print(str(block.appID))
                print(str(block.serviceID))
                print(str(block.lTAddr))
                print(str(block.sessionID))
                print(str(block.sequenceID))
            if isinstance(block, ApplicationHeaderBlock):
                print(str(block.ioType))
                print(str(block.messageType))
                print(str(block.lTAddr))
            if isinstance(block, UserHeaderBlock):
                for tag in block.tags:
                    print(str(tag))
            if isinstance(block, TextBlock):
                for tag in block.tags:
                    print(str(tag))

NOTE
============

The function to create SWIFT Message from DOM will be released soon.