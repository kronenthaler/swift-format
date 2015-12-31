__author__ = 'kronenthaler'

from SwiftTokenizer import SwiftTokenizer
from SwiftNodeTypes import *

class SwiftParser:
    # the class needs a tokenizer
    # the class needs to store the parsing tree, that will be input to the formatter

    def __init__(self, src=None):
        pass

    def comment(self, tokenizer):
        comment = self.single_line_comment(tokenizer)
        if comment:
            return comment
        return self.multi_line_comment(tokenizer)

    def single_line_comment(self, tokenizer):
        head = tokenizer.search_for(u"//")
        if not head:
            return tokenizer.push_back()

        comment = tokenizer.next_token(delimiters="\x0A\x0D")
        if not comment:
            return tokenizer.push_back()

        return SingleLineComment(comment)

    def multi_line_comment(self, tokenizer):
        head = tokenizer.search_for(u"/*")
        if not head:
            return tokenizer.push_back()

        comment = tokenizer.forward_until(u"*/")
        if not comment:
            return tokenizer.push_back()

        return MultiLineComment(comment)

