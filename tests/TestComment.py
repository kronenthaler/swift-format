import unittest
import string
from SwiftFormat.Parser import *
from SwiftFormat.Syntax import *

class CommentTest(unittest.TestCase):

    def testSingleLine(self):
        parser = comment()
        assert parser.parse(u"//something")
        assert parser.parse(u"//somethingn\n")
        assert parser.parse(u"//somethingn\r")
        assert parser.parse(u"//\n")
        assert parser.parse(u"//\r")
        assert parser.parse(u"//")

    def testMultiLine(self):
        parser = comment()
        assert parser.parse(u"/* somehting */")