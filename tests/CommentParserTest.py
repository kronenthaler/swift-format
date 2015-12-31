__author__ = 'ignacio'

__author__ = 'kronenthaler'

import unittest
import string
from SwiftFormat.SwiftTokenizer import SwiftTokenizer
from SwiftFormat.SwiftParser import SwiftParser
from SwiftFormat.SwiftNodeTypes import *

class SingleLineCommentParserTest(unittest.TestCase):
    def testIncompleteHead(self):
        tokenizer = SwiftTokenizer("/incomplete comment\n")
        parser = SwiftParser()

        assert parser.single_line_comment(tokenizer) is None

    def testWrongHead(self):
        tokenizer = SwiftTokenizer("/ /incomplete comment\n")
        parser = SwiftParser()

        assert parser.single_line_comment(tokenizer) is None

    def testWrongEOL(self):
        tokenizer = SwiftTokenizer("/incomplete comment\t")
        parser = SwiftParser()

        assert parser.single_line_comment(tokenizer) is None

    def testEOL1(self):
        tokenizer = SwiftTokenizer("//incomplete comment\x0A")
        parser = SwiftParser()

        assert parser.single_line_comment(tokenizer) is not None

    def testEOL2(self):
        tokenizer = SwiftTokenizer("//incomplete comment\x0D")
        parser = SwiftParser()

        assert parser.single_line_comment(tokenizer) is not None

    def testCorrectContent(self):
        tokenizer = SwiftTokenizer("//a comment\n")
        parser = SwiftParser()

        comment = parser.single_line_comment(tokenizer)
        assert comment is not None
        assert comment.token.cleaned_data == u'a comment'


class MultiLineCommentParserTest(unittest.TestCase):
    def testCorrectContent(self):
        tokenizer = SwiftTokenizer("/* incomplete comment */")
        parser = SwiftParser()

        comment = parser.multi_line_comment(tokenizer)
        assert comment is not None
        assert comment.token.cleaned_data == u' incomplete comment '

    def testFalseEnds(self):
        tokenizer = SwiftTokenizer("/* incomplete ** something * comment */")
        parser = SwiftParser()

        comment = parser.multi_line_comment(tokenizer)
        assert comment is not None
        assert comment.token.cleaned_data == u' incomplete ** something * comment '

    def testIncompleteHead(self):
        tokenizer = SwiftTokenizer("/ incomplete ** something * comment */")
        parser = SwiftParser()

        comment = parser.multi_line_comment(tokenizer)
        assert comment is None

    def testIncompleteTail(self):
        tokenizer = SwiftTokenizer("/* incomplete ** something * comment /")
        parser = SwiftParser()

        comment = parser.multi_line_comment(tokenizer)
        assert comment is None

    # def testNestedComments(self):
    #     tokenizer = SwiftTokenizer("/* /* incomplete ** something */ * comment */")
    #     parser = SwiftParser()
    #
    #     comment = parser.multi_line_comment(tokenizer)
    #     print comment
    #     assert comment is None

class CommentParserTests(unittest.TestCase):
    def testSingleLineComment(self):
        tokenizer = SwiftTokenizer("//a comment\n")
        parser = SwiftParser()

        comment = parser.comment(tokenizer)
        assert comment is not None
        assert isinstance(comment, SingleLineComment)
        assert comment.token.cleaned_data == "a comment"

    def testMultiLineComment(self):
        tokenizer = SwiftTokenizer("/*a comment*/")
        parser = SwiftParser()

        comment = parser.comment(tokenizer)
        assert comment is not None
        assert isinstance(comment, MultiLineComment)
        assert comment.token.cleaned_data == "a comment"

    def testNotAComment(self):
        tokenizer = SwiftTokenizer("let a = 10")
        parser = SwiftParser()

        comment = parser.comment(tokenizer)
        assert comment is None
        assert tokenizer.index == 0
