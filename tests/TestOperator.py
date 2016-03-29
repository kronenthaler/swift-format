import unittest
import string
from SwiftFormat.Syntax import *


class OperatorTest(unittest.TestCase):
    def testStandardOperators(self):
        parser = operator()
        assert parser.parse(u"+")
        assert parser.parse(u"-")
        assert parser.parse(u"/")
        assert parser.parse(u"*")
        assert parser.parse(u"%")
        assert parser.parse(u"&")
        assert parser.parse(u"^")
        assert parser.parse(u"|")
        assert parser.parse(u"?")
        assert parser.parse(u"??")
        assert parser.parse(u"~")
        assert parser.parse(u"!")
        assert parser.parse(u"=")

    def testComparisonOperators(self):
        parser = operator()
        assert parser.parse(u">")
        assert parser.parse(u">=")
        assert parser.parse(u"<")
        assert parser.parse(u"<=")
        assert parser.parse(u"==")
        assert parser.parse(u"!=")

    def testAssignmentOperators(self):
        parser = operator()
        assert parser.parse(u"+=")
        assert parser.parse(u"-=")
        assert parser.parse(u"*=")
        assert parser.parse(u"/=")
        assert parser.parse(u"%=")
        assert parser.parse(u"^=")
        assert parser.parse(u"&=")
        assert parser.parse(u"|=")
        assert parser.parse(u"~=")
        assert parser.parse(u">>=")
        assert parser.parse(u"<<=")

    def testDotOperators(self):
        parser = operator()
        assert parser.parse(u".+")
        assert parser.parse(u".-")
        assert parser.parse(u"./")
        assert parser.parse(u".*")
        assert parser.parse(u".%")
        assert parser.parse(u".&")
        assert parser.parse(u".^")
        assert parser.parse(u".|")
        assert parser.parse(u".?")
        assert parser.parse(u".~")
        assert parser.parse(u".!")
        assert parser.parse(u".=")

    def testAssignmentDotOperators(self):
        parser = operator()
        assert parser.parse(u".+=")
        assert parser.parse(u".-=")
        assert parser.parse(u".*=")
        assert parser.parse(u"./=")
        assert parser.parse(u".%=")
        assert parser.parse(u".^=")
        assert parser.parse(u".&=")
        assert parser.parse(u".|=")
        assert parser.parse(u".~=")
        assert parser.parse(u".>>=")
        assert parser.parse(u".<<=")