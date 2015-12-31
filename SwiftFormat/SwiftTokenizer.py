__author__ = 'kronenthaler'
import string

class SwiftToken:
    def __init__(self, cleaned_data, start_position, end_position):
        self.cleaned_data = cleaned_data
        self.start_position = start_position
        self.end_position = end_position

    def __str__(self):
        return "([{0} -> {1}] = {2})".format(self.start_position, self.end_position - 1, self.cleaned_data)

class SwiftTokenizer:
    def __init__(self, src):
        self.index = 0
        self.input = src
        self.on_going = []

    def next_token(self, skip=string.whitespace, delimiters=string.whitespace+"!\"#$%&'()*+,-./:;<=>?@[\]^`{|}~"):
        token_payload = u"";
        skipping = True
        for i in range(self.index, len(self.input)):
            if skipping:
                if self.input[i] not in skip:
                    skipping = False
                    token_payload += self.input[i]
                    if self.input[i] in delimiters:
                        token = SwiftToken(token_payload, self.index, i)
                        self.on_going.insert(0, token)
                        # move to the next char
                        self.index = i + 1
                        return token
            else:
                if self.input[i] in delimiters:
                    token = SwiftToken(token_payload, self.index, i)
                    self.on_going.insert(0, token)
                    self.index = i
                    return token
                token_payload += self.input[i]

        return None

    def push_back(self, last_tokens=1):
        while last_tokens > 0 and self.on_going.__len__() > 0:
            token = self.on_going.pop(0)
            self.index = token.start_position
            last_tokens -= 1

    def current_token(self):
        if self.on_going.__len__() > 0:
            return self.on_going[0]
        return None
