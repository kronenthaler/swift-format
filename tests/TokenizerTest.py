__author__ = 'kronenthaler'

import unittest
import string
from SwiftFormat.SwiftTokenizer import SwiftTokenizer

class TokenizerTests(unittest.TestCase):

    def testNextTokenPresentToken(self):
        tokenizer = SwiftTokenizer(" basic_trimmer(param1,  param2  )    {} ")

        assert tokenizer.next_token().cleaned_data == u"basic_trimmer"
        assert tokenizer.next_token().cleaned_data == u"("
        assert tokenizer.next_token().cleaned_data == u"param1"
        assert tokenizer.next_token().cleaned_data == u","
        assert tokenizer.next_token().cleaned_data == u"param2"
        assert tokenizer.next_token().cleaned_data == u")"
        assert tokenizer.next_token().cleaned_data == u"{"
        assert tokenizer.next_token().cleaned_data == u"}"
        assert tokenizer.next_token() is None

    def testPushBackSimpleToken(self):
        tokenizer = SwiftTokenizer(" basic_trimmer(param1,  param2  )    {} ")

        # control
        assert tokenizer.next_token().cleaned_data == u"basic_trimmer"

        tokenizer.push_back()
        assert tokenizer.next_token(delimiters=string.punctuation+string.whitespace).cleaned_data == u"basic"

    def testPushBackMultipleTokens(self):
        tokenizer = SwiftTokenizer(" basic_trimmer(param1,  param2  )    {} ")

        # control
        assert tokenizer.next_token().cleaned_data == u"basic_trimmer"

        tokenizer.push_back()
        assert tokenizer.next_token(delimiters=string.punctuation+string.whitespace).cleaned_data == u"basic"
        assert tokenizer.next_token(delimiters=string.punctuation+string.whitespace).cleaned_data == u"_"
        assert tokenizer.next_token(delimiters=string.punctuation+string.whitespace).cleaned_data == u"trimmer"

        tokenizer.push_back(4)
        assert tokenizer.next_token().cleaned_data == u"basic_trimmer"

    def testPushBackMultipleTokensAndForward(self):
        tokenizer = SwiftTokenizer(" basic_trimmer(param1,  param2  )    {} ")

        # control
        assert tokenizer.next_token().cleaned_data == u"basic_trimmer"

        tokenizer.push_back()
        assert tokenizer.next_token(delimiters=string.punctuation+string.whitespace).cleaned_data == u"basic"
        assert tokenizer.next_token(delimiters=string.punctuation+string.whitespace).cleaned_data == u"_"
        assert tokenizer.next_token(delimiters=string.punctuation+string.whitespace).cleaned_data == u"trimmer"

        tokenizer.push_back(2)
        assert tokenizer.next_token().cleaned_data == u"_trimmer"

    def testCurrentTokenWhenEmpty(self):
        tokenizer = SwiftTokenizer(" basic_trimmer(param1,  param2  )    {} ")

        assert tokenizer.current_token() is None

    def testCurrentTokenAfterATokenWasRetrieved(self):
        tokenizer = SwiftTokenizer(" basic_trimmer(param1,  param2  )    {} ")

        tokenizer.next_token()
        assert tokenizer.current_token() is not None
        assert tokenizer.current_token().cleaned_data == u"basic_trimmer"