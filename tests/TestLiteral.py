import unittest
import string
from SwiftFormat.Syntax import *


class LiteralTest(unittest.TestCase):

    def testNilLiteral(self):
        parser = literal()
        assert parser.parse(u"nil")
        assert parser.parse(u"nil")[0].type == SwiftTypes.LITERAL_NIL
        assert parser.parse(u"Nil") is None
        assert parser.parse(u"NIL") is None

    def testBooleanLiteral(self):
        parser = literal()
        assert parser.parse(u"true")
        assert parser.parse(u"true")[0].type == SwiftTypes.LITERAL_BOOLEAN
        assert parser.parse(u"True") is None
        assert parser.parse(u"TRUE") is None
        assert parser.parse(u"YES") is None
        assert parser.parse(u"false")
        assert parser.parse(u"false")[0].type == SwiftTypes.LITERAL_BOOLEAN
        assert parser.parse(u"False") is None
        assert parser.parse(u"FALSE") is None
        assert parser.parse(u"NO") is None

    def testBinaryLiteral(self):
        parser = literal()
        assert parser.parse(u"0b0")
        assert parser.parse(u"-0b0")
        assert parser.parse(u"0b1")
        assert parser.parse(u"-0b1")
        assert parser.parse(u"0b0001010010101")
        assert parser.parse(u"-0b0001010010101")
        assert parser.parse(u"0b0__001010010101_")
        assert parser.parse(u"-0b0__001010010101_")
        assert parser.parse(u"-0b")[0].type != SwiftTypes.LITERAL_INTEGER_BINARY
        assert parser.parse(u"-0b3")[0].type != SwiftTypes.LITERAL_INTEGER_BINARY

    def testOctalLiteral(self):
        parser = literal()
        assert parser.parse(u"0o0")
        assert parser.parse(u"-0o0")
        assert parser.parse(u"0o1")
        assert parser.parse(u"-0o1")
        assert parser.parse(u"0o0001010010101")
        assert parser.parse(u"-0o0001010010101")
        assert parser.parse(u"0o777717625521")
        assert parser.parse(u"-0o777717625521")
        assert parser.parse(u"-0o")[0].type != SwiftTypes.LITERAL_INTEGER_OCTAL
        assert parser.parse(u"-0o8")[0].type != SwiftTypes.LITERAL_INTEGER_OCTAL

    def testDecimalLiteral(self):
        parser = literal()
        assert parser.parse(u"0")
        assert parser.parse(u"-0")
        assert parser.parse(u"1")
        assert parser.parse(u"-1")
        assert parser.parse(u"0001010010101")
        assert parser.parse(u"-0001010010101")
        assert parser.parse(u"0777717625521")
        assert parser.parse(u"-0977717625521")

    def testHexadecimalLiteral(self):
        parser = literal()
        assert parser.parse(u"0x0")
        assert parser.parse(u"-0x0")
        assert parser.parse(u"0x1")
        assert parser.parse(u"-0x1")
        assert parser.parse(u"0x0001010010101")
        assert parser.parse(u"-0x0001010010101")
        assert parser.parse(u"0x777717625521")
        assert parser.parse(u"-0x777717625521")
        assert parser.parse(u"-0x")[0].type != SwiftTypes.LITERAL_INTEGER_HEXADECIMAL
        assert parser.parse(u"-0xG")[0].type != SwiftTypes.LITERAL_INTEGER_HEXADECIMAL