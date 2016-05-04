import unittest
from SwiftFormat.Syntax import *


class IdentifierTest(unittest.TestCase):
    def testImplicitParameter(self):
        parser = identifier()
        assert parser.parse(u"$0")
        assert parser.parse(u"$0")[0].meta.type == SwiftTypes.IMPLICIT_PARAMETER
        assert parser.parse(u"$1")
        assert parser.parse(u"$123123")
        assert parser.parse(u"$") is None

    def testEscapedIdentifier(self):
        parser = identifier()
        assert parser.parse(u"`valid`")
        assert parser.parse(u"`valid`")[0].meta.type == SwiftTypes.IDENTIFIER
        assert parser.parse(u"`valid") is None
        assert parser.parse(u"valid`")
        assert parser.parse(u"`0valid`") is None

    def testIdentifier(self):
        parser = identifier()
        assert parser.parse(u"valid")
        assert parser.parse(u"valid")[0].meta.type == SwiftTypes.IDENTIFIER
        assert parser.parse(u"0valid") is None
