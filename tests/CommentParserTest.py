import unittest

from SwiftFormat.Scanner.SwiftScanner import *
from SwiftFormat.SwiftNodeTypes import *
from SwiftFormat.SwiftParser import SwiftParser


class SingleLineCommentParserTest(unittest.TestCase):
    def testIncompleteHead(self):
        scanner = SwiftScanner("/incomplete comment\n")
        assert scanner.comment.single_line_comment(scanner) is None

    def testWrongHead(self):
        scanner = SwiftScanner("/ /incomplete comment\n")
        assert scanner.comment.single_line_comment(scanner) is None

    def testWrongEOL(self):
        scanner = SwiftScanner("/incomplete comment\t")
        assert scanner.comment.single_line_comment(scanner) is None

    def testEOL1(self):
        scanner = SwiftScanner("//incomplete comment\x0A")
        assert scanner.comment.single_line_comment(scanner) is not None

    def testEOL2(self):
        scanner = SwiftScanner("//incomplete comment\x0D")
        assert scanner.comment.single_line_comment(scanner) is not None

    def testEOF(self):
        scanner = SwiftScanner("//incomplete comment")
        assert scanner.comment.single_line_comment(scanner) is not None

    def testCorrectContent(self):
        scanner = SwiftScanner("//a comment\n")
        comment = scanner.comment.single_line_comment(scanner)
        assert comment is not None
        assert comment.token.token == u'a comment'


class MultiLineCommentParserTest(unittest.TestCase):
    def testCorrectContent(self):
        scanner = SwiftScanner("/* incomplete comment */")
        comment = scanner.comment.multi_line_comment(scanner)
        assert comment is not None
        assert comment.token.token == u' incomplete comment '

    def testFalseEnds(self):
        scanner = SwiftScanner("/* incomplete ** something * comment */")
        comment = scanner.comment.multi_line_comment(scanner)
        assert comment is not None
        assert comment.token.token == u' incomplete ** something * comment '

    def testIncompleteHead(self):
        scanner = SwiftScanner("/ incomplete ** something * comment */")
        comment = scanner.comment.multi_line_comment(scanner)
        assert comment is None

    def testIncompleteTail(self):
        scanner = SwiftScanner("/* incomplete ** something * comment /")
        comment = scanner.comment.multi_line_comment(scanner)
        assert comment is None

    def testNestedComments(self):
        scanner = SwiftScanner("/* /* incomplete ** something */ * comment */")
        comment = scanner.comment.multi_line_comment(scanner)
        assert comment is not None
        assert comment.children[0] == SwiftLexem(u" ", 2, 3)
        assert comment.children[1] == MultiLineComment(SwiftLexem(u" incomplete ** something ", 5, 30))
        assert comment.children[2] == SwiftLexem(u" * comment ", 32, 43)

    def testMultiComments(self):
        scanner = SwiftScanner("/* /* incomplete ** something */ * comment /*something else*/*/")
        comment = scanner.comment.multi_line_comment(scanner)
        assert comment is not None
        assert comment.children[0] == SwiftLexem(u" ", 2, 3)
        assert comment.children[1] == MultiLineComment(SwiftLexem(u" incomplete ** something ", 5, 30))
        assert comment.children[2] == SwiftLexem(u" * comment ", 32, 43)
        assert comment.children[3] == MultiLineComment(SwiftLexem(u"something else", 45, 59))


class CommentParserTests(unittest.TestCase):
    def testSingleLineComment(self):
        scanner = SwiftScanner("//a comment\n")
        comment = scanner.comment.comment(scanner)
        assert comment is not None
        assert isinstance(comment, SingleLineComment)
        assert comment.token.token == "a comment"

    def testMultiLineComment(self):
        scanner = SwiftScanner("/*a comment*/")
        comment = scanner.comment.comment(scanner)
        assert comment is not None
        assert isinstance(comment, MultiLineComment)
        assert comment.token.token == "a comment"

    def testNotAComment(self):
        scanner = SwiftScanner("let a = 10")
        comment = scanner.comment.comment(scanner)
        assert comment is None
        assert scanner.index == 0

    def testSkipComments(self):
        scanner = SwiftScanner("  /* a */ // b \n /* c */ let var = 1")
        comment = scanner.skip_comments()
        assert scanner.current_token() == SwiftLexem(u"let", 24, 28)

    def testNoSkipComments(self):
        scanner = SwiftScanner("let var = 1")
        comment = scanner.skip_comments()
        assert scanner.current_token() == SwiftLexem(u"let", 0, 3)
