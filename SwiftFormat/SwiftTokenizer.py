__author__ = 'kronenthaler'

import string

class SwiftToken:
    def __init__(self, cleaned_data, start_position, end_position):
        self.cleaned_data = cleaned_data
        self.start_position = start_position
        self.end_position = end_position
        self.type = None

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

    def search_for(self, target_token):
        if target_token is None or target_token.__len__() == 0:
            return None

        start_position = self.index
        payload = u""
        tokens_retrieved = 0
        found = True

        for i in range(0, target_token.__len__()):
            skip = string.whitespace
            if i != 0:
                skip = ""

            tok = self.next_token(delimiters="{0}".format(target_token[i]), skip=skip)

            tokens_retrieved += 1
            if tok is None or tok.cleaned_data != u"{0}".format(target_token[i]):
                found = False
                break

            payload += tok.cleaned_data

        if found:
            token = SwiftToken(payload, start_position, self.index)
            # discard the partial tokens and group them as 1
            self.discard_tokens(tokens_retrieved)
            self.on_going.insert(0, token)
            return token

        self.push_back(tokens_retrieved)

    def forward_until(self, target_token):
        if target_token is None or target_token.__len__() == 0:
            return None

        start_position = self.index
        payload = u""

        # forward to the first candidate of the token
        for i in range(self.index, len(self.input)):
            if self.input[i] == target_token[0]:
                found = True
                for j in range(1, target_token.__len__()):
                    if self.input[j + i] != target_token[j]:
                        found = False
                        break

                if found:
                    token = SwiftToken(payload, start_position, i)
                    self.on_going.insert(0, token)
                    self.index = i + target_token.__len__()
                    return token
                else:
                    payload += self.input[i]
            else:
                payload += self.input[i]

        return None

    def discard_tokens(self, last_tokens=1):
        while last_tokens > 0 and self.on_going.__len__() > 0:
            token = self.on_going.pop(0)
            last_tokens -= 1

    def push_back(self, last_tokens=1):
        while last_tokens > 0 and self.on_going.__len__() > 0:
            token = self.on_going.pop(0)
            self.index = token.start_position
            last_tokens -= 1

        return None

    def current_token(self):
        if self.on_going.__len__() > 0:
            return self.on_going[0]
        return None
