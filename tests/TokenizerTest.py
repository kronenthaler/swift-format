__author__ = 'kronenthaler'

import unittest
from SwiftFormat.SwiftTokenizer import SwiftTokenizer

class TokenizerTests(unittest.TestCase):

    def testNextTokenPresentToken(self):
        tokenizer = SwiftTokenizer(" basic_trimmer(param1,  param2  )    {} ")

        assert tokenizer.next_token() == u"basic_trimmer"
        assert tokenizer.next_token() == u"param1"
        assert tokenizer.next_token() == u"param2"
        assert tokenizer.next_token() == None

