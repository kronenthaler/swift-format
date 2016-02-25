import unittest
import json
from SwiftFormat.Parser import *
from SwiftFormat.Syntax import *


class CommentTest(unittest.TestCase):

    def testSingleLine(self):
        parser = comment()
        assert parser.parse(u"//something\n")
        assert parser.parse(u"//something\r")
        assert parser.parse(u"//something")
        assert parser.parse(u"//\n")
        assert parser.parse(u"//\r")
        assert parser.parse(u"//")
        assert parser.parse(u"/asd\n") is None

    def testMultiLine(self):
        parser = comment()
        assert parser.parse(u"/* something */")
        assert parser.parse(u"/* something ** something * comment */")
        assert parser.parse(u"/**/")
        assert parser.parse(u"/* something") is None
        assert parser.parse(u"/* something *") is None
        assert parser.parse(u"/ something */") is None

    def testMultiLineNested(self):
        parser = comment()
        assert parser.parse(u"/*/*/**/*/*/")
        assert parser.parse(u"/* something /* something /* something */ */ */")
        assert parser.parse(u"/* something /* something */ /* something */ */")
        assert parser.parse(u"/* /* something */ /* something */ something */")