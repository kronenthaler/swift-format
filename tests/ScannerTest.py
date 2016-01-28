import string
import unittest

from SwiftFormat.Scanner.SwiftScanner import SwiftScanner
from SwiftFormat.Scanner.SwiftLexem import SwiftLexem

class TokenizerTests(unittest.TestCase):

    def testNextTokenPresentToken(self):
        tokenizer = SwiftScanner(" basic_trimmer(param1,  param2  )    {} ")

        assert tokenizer.next_chunk().token == u"basic_trimmer"
        assert tokenizer.next_chunk().token == u"("
        assert tokenizer.next_chunk().token == u"param1"
        assert tokenizer.next_chunk().token == u","
        assert tokenizer.next_chunk().token == u"param2"
        assert tokenizer.next_chunk().token == u")"
        assert tokenizer.next_chunk().token == u"{"
        assert tokenizer.next_chunk().token == u"}"
        assert tokenizer.next_chunk() is None

    def testPushBackSimpleToken(self):
        tokenizer = SwiftScanner(" basic_trimmer(param1,  param2  )    {} ")

        # control
        assert tokenizer.next_chunk().token == u"basic_trimmer"

        tokenizer.push_back()
        assert tokenizer.next_chunk(delimiters=string.punctuation + string.whitespace).token == u"basic"

    def testPushBackMultipleTokens(self):
        tokenizer = SwiftScanner(" basic_trimmer(param1,  param2  )    {} ")

        # control
        assert tokenizer.next_chunk().token == u"basic_trimmer"

        tokenizer.push_back()
        assert tokenizer.next_chunk(delimiters=string.punctuation + string.whitespace).token == u"basic"
        assert tokenizer.next_chunk(delimiters=string.punctuation + string.whitespace).token == u"_"
        assert tokenizer.next_chunk(delimiters=string.punctuation + string.whitespace).token == u"trimmer"

        tokenizer.push_back(4)
        assert tokenizer.next_chunk().token == u"basic_trimmer"

    def testPushBackMultipleTokensAndForward(self):
        tokenizer = SwiftScanner(" basic_trimmer(param1,  param2  )    {} ")

        # control
        assert tokenizer.next_chunk().token == u"basic_trimmer"

        tokenizer.push_back()
        assert tokenizer.next_chunk(delimiters=string.punctuation + string.whitespace).token == u"basic"
        assert tokenizer.next_chunk(delimiters=string.punctuation + string.whitespace).token == u"_"
        assert tokenizer.next_chunk(delimiters=string.punctuation + string.whitespace).token == u"trimmer"

        tokenizer.push_back(2)
        assert tokenizer.next_chunk().token == u"_trimmer"

    def testCurrentTokenWhenEmpty(self):
        tokenizer = SwiftScanner(" basic_trimmer(param1,  param2  )    {} ")

        assert tokenizer.current_token() is None

    def testCurrentTokenAfterATokenWasRetrieved(self):
        tokenizer = SwiftScanner(" basic_trimmer(param1,  param2  )    {} ")

        tokenizer.next_chunk()
        assert tokenizer.current_token() is not None
        assert tokenizer.current_token().token == u"basic_trimmer"

    def testIdentifierWithComments(self):
        tokenizer = SwiftScanner(" /* this is an ID */ // something else \n my_var_name_01");
        token = tokenizer.next_token()
        assert token.token == u'my_var_name_01'
        assert token.type == SwiftLexem.IDENTIFIER
        assert token.prefix_comments.__len__() == 2
        assert token.prefix_comments[0].__repr__() == u"/* this is an ID */"
        assert token.prefix_comments[1].__repr__() == u"// something else \n"