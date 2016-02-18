# TODO: adapt tests, the cases are still valid
import unittest

from SwiftFormat.Scanner.SwiftScanner import *
from SwiftFormat.SwiftNodeTypes import *
from SwiftFormat.SwiftParser import SwiftParser


class IdentifierParserTest(unittest.TestCase):
    def testImplicitParameter(self):
        scanner = SwiftScanner(u'$10002 ')
        identifier = IdentifierScanner()
        lexeme = identifier.identifier(scanner)
        assert lexeme.token == u'$10002'
        assert lexeme.type == SwiftLexem.IMPLICIT_PARAMETER

    def testIdentifierSingleCharacter(self):
        scanner = SwiftScanner(u'a ')
        identifier = IdentifierScanner()
        lexeme = identifier.identifier(scanner)
        assert lexeme.token == u'a'
        assert lexeme.type == SwiftLexem.IDENTIFIER

    def testIdentifierMultiCharacterCharacter(self):
        scanner = SwiftScanner(u'magic ')
        identifier = IdentifierScanner()
        lexeme = identifier.identifier(scanner)
        assert lexeme.token == u'magic'
        assert lexeme.type == SwiftLexem.IDENTIFIER

    def testIdentifierEscapedCharacterCharacter(self):
        scanner = SwiftScanner(u'`magic` ')
        identifier = IdentifierScanner()
        lexeme = identifier.identifier(scanner)
        assert lexeme.token == u'`magic`'
        assert lexeme.type == SwiftLexem.IDENTIFIER

    def testBrokenIdentifierEscapedCharacterCharacter(self):
        scanner = SwiftScanner(u'`magic ')
        identifier = IdentifierScanner()
        lexeme = identifier.identifier(scanner)
        assert lexeme is None

    def testBrokenStartIdentifier(self):
        scanner = SwiftScanner(u'0magic ')
        identifier = IdentifierScanner()
        lexeme = identifier.identifier(scanner)
        assert lexeme is None

    def testBrokenStartIdentifierQuoted(self):
        scanner = SwiftScanner(u'`0magic` ')
        identifier = IdentifierScanner()
        lexeme = identifier.identifier(scanner)
        assert lexeme is None

    def testSingleCharacterIdentifierEOF(self):
        scanner = SwiftScanner(u'a')
        identifier = IdentifierScanner()
        lexeme = identifier.identifier(scanner)
        assert lexeme.token == u'a'
        assert lexeme.type == SwiftLexem.IDENTIFIER