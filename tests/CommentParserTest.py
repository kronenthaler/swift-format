import unittest
import string
from SwiftFormat.SwiftTokenizer import *
from SwiftFormat.SwiftParser import SwiftParser
from SwiftFormat.SwiftNodeTypes import *


class SingleLineCommentParserTest(unittest.TestCase):
    def testIncompleteHead(self):
        tokenizer = SwiftTokenizer("/incomplete comment\n")
        parser = SwiftParser()

        assert parser.comment.single_line_comment(tokenizer) is None

    def testWrongHead(self):
        tokenizer = SwiftTokenizer("/ /incomplete comment\n")
        parser = SwiftParser()

        assert parser.comment.single_line_comment(tokenizer) is None

    def testWrongEOL(self):
        tokenizer = SwiftTokenizer("/incomplete comment\t")
        parser = SwiftParser()

        assert parser.comment.single_line_comment(tokenizer) is None

    def testEOL1(self):
        tokenizer = SwiftTokenizer("//incomplete comment\x0A")
        parser = SwiftParser()

        assert parser.comment.single_line_comment(tokenizer) is not None

    def testEOL2(self):
        tokenizer = SwiftTokenizer("//incomplete comment\x0D")
        parser = SwiftParser()

        assert parser.comment.single_line_comment(tokenizer) is not None

    def testEOF(self):
        tokenizer = SwiftTokenizer("//incomplete comment")
        parser = SwiftParser()

        assert parser.comment.single_line_comment(tokenizer) is not None

    def testCorrectContent(self):
        tokenizer = SwiftTokenizer("//a comment\n")
        parser = SwiftParser()

        comment = parser.comment.single_line_comment(tokenizer)
        assert comment is not None
        assert comment.token.cleaned_data == u'a comment'


class MultiLineCommentParserTest(unittest.TestCase):
    def testCorrectContent(self):
        tokenizer = SwiftTokenizer("/* incomplete comment */")
        parser = SwiftParser()

        comment = parser.comment.multi_line_comment(tokenizer)
        assert comment is not None
        assert comment.token.cleaned_data == u' incomplete comment '

    def testFalseEnds(self):
        tokenizer = SwiftTokenizer("/* incomplete ** something * comment */")
        parser = SwiftParser()

        comment = parser.comment.multi_line_comment(tokenizer)
        assert comment is not None
        assert comment.token.cleaned_data == u' incomplete ** something * comment '

    def testIncompleteHead(self):
        tokenizer = SwiftTokenizer("/ incomplete ** something * comment */")
        parser = SwiftParser()

        comment = parser.comment.multi_line_comment(tokenizer)
        assert comment is None

    def testIncompleteTail(self):
        tokenizer = SwiftTokenizer("/* incomplete ** something * comment /")
        parser = SwiftParser()

        comment = parser.comment.multi_line_comment(tokenizer)
        assert comment is None

    def testNestedComments(self):
        tokenizer = SwiftTokenizer("/* /* incomplete ** something */ * comment */")
        parser = SwiftParser()

        comment = parser.comment.multi_line_comment(tokenizer)
        assert comment is not None
        assert comment.children[0] == SwiftToken(u" ", 2, 3)
        assert comment.children[1] == MultiLineComment(SwiftToken(u" incomplete ** something ", 5, 30))
        assert comment.children[2] == SwiftToken(u" * comment ", 32, 43)

    def testMultiComments(self):
        tokenizer = SwiftTokenizer("/* /* incomplete ** something */ * comment /*something else*/*/")
        parser = SwiftParser()

        comment = parser.comment.multi_line_comment(tokenizer)
        assert comment is not None
        assert comment.children[0] == SwiftToken(u" ", 2, 3)
        assert comment.children[1] == MultiLineComment(SwiftToken(u" incomplete ** something ", 5, 30))
        assert comment.children[2] == SwiftToken(u" * comment ", 32, 43)
        assert comment.children[3] == MultiLineComment(SwiftToken(u"something else", 45, 59))


class CommentParserTests(unittest.TestCase):
    def testSingleLineComment(self):
        tokenizer = SwiftTokenizer("//a comment\n")
        parser = SwiftParser()

        comment = parser.comment.comment(tokenizer)
        assert comment is not None
        assert isinstance(comment, SingleLineComment)
        assert comment.token.cleaned_data == "a comment"

    def testMultiLineComment(self):
        tokenizer = SwiftTokenizer("/*a comment*/")
        parser = SwiftParser()

        comment = parser.comment.comment(tokenizer)
        assert comment is not None
        assert isinstance(comment, MultiLineComment)
        assert comment.token.cleaned_data == "a comment"

    def testNotAComment(self):
        tokenizer = SwiftTokenizer("let a = 10")
        parser = SwiftParser()

        comment = parser.comment.comment(tokenizer)
        assert comment is None
        assert tokenizer.index == 0

    def testSkipComments(self):
        tokenizer = SwiftTokenizer("  /* a */ // b \n /* c */ let var = 1")
        parser = SwiftParser()

        comment = parser.skip_comments(tokenizer)
        assert tokenizer.current_token() == SwiftToken(u"let", 24, 28)

    def testNoSkipComments(self):
        tokenizer = SwiftTokenizer("let var = 1")
        parser = SwiftParser()

        comment = parser.skip_comments(tokenizer)
        assert tokenizer.current_token() == SwiftToken(u"let", 0, 3)
