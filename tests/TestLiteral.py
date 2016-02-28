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
        assert parser.parse(u"0b0")[0].type == SwiftTypes.LITERAL_INTEGER_BINARY
        assert parser.parse(u"-0b0")
        assert parser.parse(u"0b1")
        assert parser.parse(u"-0b1")
        assert parser.parse(u"0b0001010010101")
        assert parser.parse(u"-0b0001010010101")
        assert parser.parse(u"0b0__001010010101_")
        assert parser.parse(u"-0b0__001010010101_")
        assert parser.parse(u"-0b__001010010101_")[0].type != SwiftTypes.LITERAL_INTEGER_BINARY
        assert parser.parse(u"-0b")[0].type != SwiftTypes.LITERAL_INTEGER_BINARY
        assert parser.parse(u"-0b3")[0].type != SwiftTypes.LITERAL_INTEGER_BINARY

    def testOctalLiteral(self):
        parser = literal()
        assert parser.parse(u"0o0")
        assert parser.parse(u"0o0")[0].type == SwiftTypes.LITERAL_INTEGER_OCTAL
        assert parser.parse(u"-0o0")
        assert parser.parse(u"0o1")
        assert parser.parse(u"-0o1")
        assert parser.parse(u"0o0001010010101")
        assert parser.parse(u"-0o0001010010101")
        assert parser.parse(u"0o777717625521")
        assert parser.parse(u"-0o777717625521")
        assert parser.parse(u"-0o777717__6255__21")
        assert parser.parse(u"-0o_777717__6255__21")[0].type != SwiftTypes.LITERAL_INTEGER_OCTAL
        assert parser.parse(u"-0o")[0].type != SwiftTypes.LITERAL_INTEGER_OCTAL
        assert parser.parse(u"-0o8")[0].type != SwiftTypes.LITERAL_INTEGER_OCTAL

    def testDecimalLiteral(self):
        parser = literal()
        assert parser.parse(u"0")
        assert parser.parse(u"0")[0].type == SwiftTypes.LITERAL_INTEGER_DECIMAL
        assert parser.parse(u"-0")
        assert parser.parse(u"1")
        assert parser.parse(u"-1")
        assert parser.parse(u"0001010010101")
        assert parser.parse(u"-0001010010101")
        assert parser.parse(u"0777717625521")
        assert parser.parse(u"-0977717625521")
        assert parser.parse(u"-09__7771762552__1")
        assert parser.parse(u"-__7771762552__1") is None

    def testHexadecimalLiteral(self):
        parser = literal()
        assert parser.parse(u"0x0")
        assert parser.parse(u"0x0")[0].type == SwiftTypes.LITERAL_INTEGER_HEXADECIMAL
        assert parser.parse(u"-0x0")
        assert parser.parse(u"0x1")
        assert parser.parse(u"-0x1")
        assert parser.parse(u"0x0001010010101")
        assert parser.parse(u"-0x0001010010101")
        assert parser.parse(u"0x777717625521")
        assert parser.parse(u"-0x777717625521")
        assert parser.parse(u"-0xafefFAECBDB")
        assert parser.parse(u"-0xa__fefFAECBD__B")
        assert parser.parse(u"-0x_a__fefFAECBD__B")[0].type != SwiftTypes.LITERAL_INTEGER_HEXADECIMAL
        assert parser.parse(u"-0x")[0].type != SwiftTypes.LITERAL_INTEGER_HEXADECIMAL
        assert parser.parse(u"-0xG")[0].type != SwiftTypes.LITERAL_INTEGER_HEXADECIMAL

    def testDecimalFloat(self):
        parser = literal()
        assert parser.parse(u"10000.0")
        assert parser.parse(u"10000.0")[0].type == SwiftTypes.LITERAL_FLOATING_DECIMAL
        assert parser.parse(u"10000.0e1")
        assert parser.parse(u"10000e1")
        assert parser.parse(u"10000.0e-1")
        assert parser.parse(u"10000.0e100")
        assert parser.parse(u"10000.0e-100")
        assert parser.parse(u".0e1") is None

    def testHexadecimalFloat(self):
        parser = literal()
        assert parser.parse(u"0x10000.0p10")
        assert parser.parse(u"0x10000.0p10")[0].type == SwiftTypes.LITERAL_FLOATING_HEXADECIMAL
        assert parser.parse(u"0x10000.0p1")
        assert parser.parse(u"0x10000p1")
        assert parser.parse(u"0x10000.0p-1")
        assert parser.parse(u"0x10000.0p100")
        assert parser.parse(u"0x10000.0p-100")
        assert parser.parse(u".0p1") is None
        assert parser.parse(u"0x0.0p1")[0].type != SwiftTypes.LITERAL_FLOATING_DECIMAL
        assert parser.parse(u"0x0p1")[0].type != SwiftTypes.LITERAL_FLOATING_DECIMAL

    def testStaticString(self):
        parser = literal()
        assert parser.parse(u'""')
        assert parser.parse(u'"aaa"')
        assert parser.parse(u'"!@#$%^&*()_+=-<>,./?:"|;`~aa"')
        assert parser.parse(u'"\n"') is None
        assert parser.parse(u'"\r"') is None
        assert parser.parse(u'"\\"') is None
        assert parser.parse(u'"\\""')
        assert parser.parse(u'"\\u{1}"')
        assert parser.parse(u'"\\u1"') is None
        assert parser.parse(u'"\\u{12}"')
        assert parser.parse(u'"\\u{123}"')
        assert parser.parse(u'"\\u{1234}"')
        assert parser.parse(u'"\\u{12345}"')
        assert parser.parse(u'"\\u{123456}"')
        assert parser.parse(u'"\\u{1234567}"')
        assert parser.parse(u'"\\u{12345678}"')
        assert parser.parse(u'"\\u{123456789}"') is None

    # def testInterpolatedString(self):
    #     parser = literal()
    #     assert parser.parse(u'"\\(something)"')
    #     assert parser.parse(u'"\\(something"') is None
