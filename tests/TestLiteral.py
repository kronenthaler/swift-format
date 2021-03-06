import unittest
import string
from SwiftFormat.Syntax import *


class LiteralTest(unittest.TestCase):
    def testNilLiteral(self):
        parser = literal()
        assert parser.parse(u"nil")
        assert parser.parse(u"nil")[0].meta.type == SwiftTypes.LITERAL_NIL
        assert parser.parse(u"Nil") is None
        assert parser.parse(u"NIL") is None

    def testBooleanLiteral(self):
        parser = literal()
        assert parser.parse(u"true")
        assert parser.parse(u"true")[0].meta.type == SwiftTypes.LITERAL_BOOLEAN
        assert parser.parse(u"True") is None
        assert parser.parse(u"TRUE") is None
        assert parser.parse(u"YES") is None
        assert parser.parse(u"false")
        assert parser.parse(u"false")[0].meta.type == SwiftTypes.LITERAL_BOOLEAN
        assert parser.parse(u"False") is None
        assert parser.parse(u"FALSE") is None
        assert parser.parse(u"NO") is None

    def testBinaryLiteral(self):
        parser = literal()
        assert parser.parse(u"0b0")
        assert parser.parse(u"0b0")[0].meta.type == SwiftTypes.LITERAL_INTEGER_BINARY
        assert parser.parse(u"-0b0")
        assert parser.parse(u"0b1")
        assert parser.parse(u"-0b1")
        assert parser.parse(u"0b0001010010101")
        assert parser.parse(u"-0b0001010010101")
        assert parser.parse(u"0b0__001010010101_")
        assert parser.parse(u"-0b0__001010010101_")
        assert parser.parse(u"-0b__001010010101_")[0].meta.type != SwiftTypes.LITERAL_INTEGER_BINARY
        assert parser.parse(u"-0b")[0].meta.type != SwiftTypes.LITERAL_INTEGER_BINARY
        assert parser.parse(u"-0b3")[0].meta.type != SwiftTypes.LITERAL_INTEGER_BINARY

    def testOctalLiteral(self):
        parser = literal()
        assert parser.parse(u"0o0")
        assert parser.parse(u"0o0")[0].meta.type == SwiftTypes.LITERAL_INTEGER_OCTAL
        assert parser.parse(u"-0o0")
        assert parser.parse(u"0o1")
        assert parser.parse(u"-0o1")
        assert parser.parse(u"0o0001010010101")
        assert parser.parse(u"-0o0001010010101")
        assert parser.parse(u"0o777717625521")
        assert parser.parse(u"-0o777717625521")
        assert parser.parse(u"-0o777717__6255__21")
        assert parser.parse(u"-0o_777717__6255__21")[0].meta.type != SwiftTypes.LITERAL_INTEGER_OCTAL
        assert parser.parse(u"-0o")[0].meta.type != SwiftTypes.LITERAL_INTEGER_OCTAL
        assert parser.parse(u"-0o8")[0].meta.type != SwiftTypes.LITERAL_INTEGER_OCTAL

    def testDecimalLiteral(self):
        parser = literal()
        assert parser.parse(u"0")
        self.assertEqual(parser.parse(u"0")[0].meta.type, SwiftTypes.LITERAL_INTEGER_DECIMAL)
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
        assert parser.parse(u"0x0")[0].meta.type == SwiftTypes.LITERAL_INTEGER_HEXADECIMAL
        assert parser.parse(u"-0x0")
        assert parser.parse(u"0x1")
        assert parser.parse(u"-0x1")
        assert parser.parse(u"0x0001010010101")
        assert parser.parse(u"-0x0001010010101")
        assert parser.parse(u"0x777717625521")
        assert parser.parse(u"-0x777717625521")
        assert parser.parse(u"-0xafefFAECBDB")
        assert parser.parse(u"-0xa__fefFAECBD__B")
        assert parser.parse(u"-0x_a__fefFAECBD__B")[0].meta.type != SwiftTypes.LITERAL_INTEGER_HEXADECIMAL
        assert parser.parse(u"-0x")[0].meta.type != SwiftTypes.LITERAL_INTEGER_HEXADECIMAL
        assert parser.parse(u"-0xG")[0].meta.type != SwiftTypes.LITERAL_INTEGER_HEXADECIMAL

    def testDecimalFloat(self):
        parser = literal()
        assert parser.parse(u"10000.0")
        assert parser.parse(u"10000.0")[0].meta.type == SwiftTypes.LITERAL_FLOATING_DECIMAL
        assert parser.parse(u"10000.0e1")
        assert parser.parse(u"10000e1")
        assert parser.parse(u"10000.0e-1")
        assert parser.parse(u"10000.0e100")
        assert parser.parse(u"10000.0e-100")
        assert parser.parse(u".0e1") is None

    def testHexadecimalFloat(self):
        parser = literal()
        assert parser.parse(u"0x10000.0p10")
        assert parser.parse(u"0x10000.0p10")[0].meta.type == SwiftTypes.LITERAL_FLOATING_HEXADECIMAL
        assert parser.parse(u"0x10000.0p1")
        assert parser.parse(u"0x10000p1")
        assert parser.parse(u"0x10000.0p-1")
        assert parser.parse(u"0x10000.0p100")
        assert parser.parse(u"0x10000.0p-100")
        assert parser.parse(u".0p1") is None
        assert parser.parse(u"0x0.0p1")[0].meta.type != SwiftTypes.LITERAL_FLOATING_DECIMAL
        assert parser.parse(u"0x0p1")[0].meta.type != SwiftTypes.LITERAL_FLOATING_DECIMAL

    def testStaticString(self):
        parser = literal()

        file = open('data-samples/valid-static-strings.txt')
        for line in file.readlines():
            self.assertIsNot(parser.parse(line), None, "is a valid string: {0}".format(line))

    def testInvalidStaticString(self):
        parser = literal()
        assert parser.parse(u'"\n"') is None
        assert parser.parse(u'"\r"') is None
        assert parser.parse(u'"\\"') is None

        file = open('data-samples/invalid-static-strings.txt')
        for line in file.readlines():
            self.assertIs(parser.parse(line), None, "is an invalid string: {0}".format(line))

    def testInterpolatedString(self):
        parser = literal()
        file = open('data-samples/valid-interpolated-strings.txt')
        for line in file.readlines():
            self.assertIsNot(parser.parse(line), None, "is a valid string: {0}".format(line))

    def testInvalidInterpolatedString(self):
        parser = literal()
        file = open('data-samples/invalid-interpolated-strings.txt')
        for line in file.readlines():
            self.assertIs(parser.parse(line), None, "is an invalid string: {0}".format(line))
