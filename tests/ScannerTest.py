import string
import unittest

from SwiftFormat.Scanner.SwiftScanner import SwiftScanner


class TokenizerTests(unittest.TestCase):

    def testNextTokenPresentToken(self):
        tokenizer = SwiftScanner(" basic_trimmer(param1,  param2  )    {} ")

        assert tokenizer._next_token().token == u"basic_trimmer"
        assert tokenizer._next_token().token == u"("
        assert tokenizer._next_token().token == u"param1"
        assert tokenizer._next_token().token == u","
        assert tokenizer._next_token().token == u"param2"
        assert tokenizer._next_token().token == u")"
        assert tokenizer._next_token().token == u"{"
        assert tokenizer._next_token().token == u"}"
        assert tokenizer._next_token() is None

    def testPushBackSimpleToken(self):
        tokenizer = SwiftScanner(" basic_trimmer(param1,  param2  )    {} ")

        # control
        assert tokenizer._next_token().token == u"basic_trimmer"

        tokenizer.push_back()
        assert tokenizer._next_token(delimiters=string.punctuation + string.whitespace).token == u"basic"

    def testPushBackMultipleTokens(self):
        tokenizer = SwiftScanner(" basic_trimmer(param1,  param2  )    {} ")

        # control
        assert tokenizer._next_token().token == u"basic_trimmer"

        tokenizer.push_back()
        assert tokenizer._next_token(delimiters=string.punctuation + string.whitespace).token == u"basic"
        assert tokenizer._next_token(delimiters=string.punctuation + string.whitespace).token == u"_"
        assert tokenizer._next_token(delimiters=string.punctuation + string.whitespace).token == u"trimmer"

        tokenizer.push_back(4)
        assert tokenizer._next_token().token == u"basic_trimmer"

    def testPushBackMultipleTokensAndForward(self):
        tokenizer = SwiftScanner(" basic_trimmer(param1,  param2  )    {} ")

        # control
        assert tokenizer._next_token().token == u"basic_trimmer"

        tokenizer.push_back()
        assert tokenizer._next_token(delimiters=string.punctuation + string.whitespace).token == u"basic"
        assert tokenizer._next_token(delimiters=string.punctuation + string.whitespace).token == u"_"
        assert tokenizer._next_token(delimiters=string.punctuation + string.whitespace).token == u"trimmer"

        tokenizer.push_back(2)
        assert tokenizer._next_token().token == u"_trimmer"

    def testCurrentTokenWhenEmpty(self):
        tokenizer = SwiftScanner(" basic_trimmer(param1,  param2  )    {} ")

        assert tokenizer.current_token() is None

    def testCurrentTokenAfterATokenWasRetrieved(self):
        tokenizer = SwiftScanner(" basic_trimmer(param1,  param2  )    {} ")

        tokenizer._next_token()
        assert tokenizer.current_token() is not None
        assert tokenizer.current_token().token == u"basic_trimmer"