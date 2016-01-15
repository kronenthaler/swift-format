from SwiftTokenizer import SwiftTokenizer
from SwiftNodeTypes import *
from Syntax import *

class SwiftParser:
    # the class needs a tokenizer
    # the class needs to store the parsing tree, that will be input to the formatter

    def __init__(self, src=None):
        self.comment = Comment()

    def skip_comments(self, tokenizer):
        tokens = []

        # skip all whitespaces, and comments until the next relevant token is found
        while True:
            token = tokenizer.next_token()
            if token.cleaned_data != u"/":
                break

            tokenizer.push_back()
            comment = self.comment.comment(tokenizer)
            if comment is None:
                break

            # take the comment element and add it to the queue of tokens
            tokens.append(comment)

        return tokens