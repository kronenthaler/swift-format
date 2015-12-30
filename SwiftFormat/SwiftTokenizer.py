__author__ = 'kronenthaler'
import string

class SwiftTokenizer:
    def __init__(self, src):
        self.index = 0
        self.input = src
        self.on_going = []

    def next_token(self, delimiters=string.whitespace+"!\"#$%&'()*+,-./:;<=>?@[\]^`{|}~"):
        # string.punctuation \ { _ }
        # give the next token until one of the delimiters are found, move the index for the next token
        token = u"";
        skipping = True
        for i in range(self.index, len(self.input)):
            if skipping:
                if self.input[i] not in delimiters:
                    skipping = False
                    token += self.input[i]
            else:
                if self.input[i] in delimiters:
                    metadata = (self.index, token, i)
                    self.on_going.insert(0,metadata)
                    self.index = i
                    return token
                token += self.input[i]

        return None

    def push_back(self, last_tokens=1):
        # check remove the token metadata from the stack, revert the index to the previous token position
        # repeat as many times as last_tokens says or the stack is empty
        pass