import unittest

from SwiftFormat.Scanner.SwiftScanner import *
from SwiftFormat.SwiftNodeTypes import *
from SwiftFormat.SwiftParser import SwiftParser


class IdentifierParserTest(unittest.TestCase):
    def testImplicitParameter(self):
        scanner = SwiftScanner(u'$10002 ')
        identifier = IdentifierScanner()
        lexem = identifier.identifier(scanner)
        assert lexem.token == u'$10002'
        assert lexem.type == SwiftLexem.IMPLICIT_PARAMETER

    def testIdentifierSingleCharacter(self):
        scanner = SwiftScanner(u'a ')
        identifier = IdentifierScanner()
        lexem = identifier.identifier(scanner)
        assert lexem.token == u'a'
        assert lexem.type == SwiftLexem.IDENTIFIER

    def testIdentifierMultiCharacterCharacter(self):
        scanner = SwiftScanner(u'magic ')
        identifier = IdentifierScanner()
        lexem = identifier.identifier(scanner)
        assert lexem.token == u'magic'
        assert lexem.type == SwiftLexem.IDENTIFIER

    def testIdentifierEscapedCharacterCharacter(self):
        scanner = SwiftScanner(u'`magic` ')
        identifier = IdentifierScanner()
        lexem = identifier.identifier(scanner)
        assert lexem.token == u'`magic`'
        assert lexem.type == SwiftLexem.IDENTIFIER

    def testBrokenIdentifierEscapedCharacterCharacter(self):
        scanner = SwiftScanner(u'`magic ')
        identifier = IdentifierScanner()
        lexem = identifier.identifier(scanner)
        assert lexem is None

    def testBrokenStartIdentifier(self):
        scanner = SwiftScanner(u'0magic ')
        identifier = IdentifierScanner()
        lexem = identifier.identifier(scanner)
        assert lexem is None

    def testBrokenStartIdentifierQuoted(self):
        scanner = SwiftScanner(u'`0magic` ')
        identifier = IdentifierScanner()
        lexem = identifier.identifier(scanner)
        assert lexem is None

    def testSingleCharacterIdentifierEOF(self):
        scanner = SwiftScanner(u'a')
        identifier = IdentifierScanner()
        lexem = identifier.identifier(scanner)
        assert lexem.token == u'a'
        assert lexem.type == SwiftLexem.IDENTIFIER