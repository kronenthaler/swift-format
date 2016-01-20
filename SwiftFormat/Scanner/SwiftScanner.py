import string
# from SwiftFormat.SwiftNodeTypes import *
from SwiftFormat.Scanner.CommentScanner import *
from SwiftFormat.Scanner.IdentifierScanner import *


class SwiftLexem:
    def __init__(self, cleaned_data, start_position, end_position):
        self.token = cleaned_data
        self.start_position = start_position
        self.end_position = end_position
        self.type = None
        self.prefix_comments = []

    def __str__(self):
        return "([{0} -> {1}] = {2})".format(self.start_position, self.end_position, self.token)

    def __repr__(self):
        return self.token

    def __eq__(self, other):
        return self.token == other.token and \
               self.start_position == other.start_position and \
               self.end_position == other.end_position


class SwiftScanner:
    def __init__(self, src):
        self.index = 0
        self.input = src
        self.on_going = []
        self.comment = CommentScanner()
        self.identifier = IdentifierScanner()

    def next_token(self):
        # retrieve the actual next token after remove whitespaces and comments
        # token ::= { comment }* expr
        # expr ::= keyword | operator | identifier | literal | symbol | EOF
        # keyword ::= let if while do else class protocol ...
        # operator ::= <use apple's grammar for operators>
        # literal ::= <use apple's grammar for literals>
        # identifier ::= <use apple's grammar for identifier>
        # symbol ::= <any other case>
        prefix_comments = self.skip_comments()

        pass

    def _next_token(self, skip=string.whitespace, delimiters=string.whitespace + "!\"#$%&'()*+,-./:;<=>?@[\]^`{|}~", allowEOF=False):
        token_payload = u""
        skipping = True
        for i in range(self.index, len(self.input)):
            if skipping:
                if self.input[i] not in skip:
                    skipping = False
                    token_payload += self.input[i]
                    if self.input[i] in delimiters:
                        token = SwiftLexem(token_payload, self.index, i)
                        self.on_going.insert(0, token)
                        # move to the next char
                        self.index = i + 1
                        return token
            else:
                if self.input[i] in delimiters:
                    token = SwiftLexem(token_payload, self.index, i)
                    self.on_going.insert(0, token)
                    self.index = i
                    return token
                token_payload += self.input[i]

        if allowEOF:
            token = SwiftLexem(token_payload, self.index, i)
            self.on_going.insert(0, token)
            self.index = i
            return token

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

            tok = self._next_token(delimiters="{0}".format(target_token[i]), skip=skip)

            tokens_retrieved += 1
            if tok is None or tok.token != u"{0}".format(target_token[i]):
                found = False
                break

            payload += tok.token

        if found:
            token = SwiftLexem(payload, start_position, self.index)
            # discard the partial tokens and group them as 1
            self.discard_tokens(tokens_retrieved)
            self.on_going.insert(0, token)
            return token

        self.push_back(tokens_retrieved)

    def advance(self, target_token):
        if target_token is None or len(target_token) == 0:
            return None

        if not isinstance(target_token, list):
            target_token = [target_token]

        start_position = self.index
        payload = u""

        # forward to the first candidate of the token
        for i in range(self.index, len(self.input)):
            for potential_token in target_token:
                if self.input[i] == potential_token[0]:
                    found = True
                    for j in range(1, potential_token.__len__()):
                        if j + i >= len(self.input) or self.input[j + i] != potential_token[j]:
                            found = False
                            break

                    if found:
                        token = SwiftLexem(payload, start_position, i)
                        self.on_going.insert(0, token)
                        self.on_going.insert(0, SwiftLexem(potential_token, i, i + potential_token.__len__()))
                        self.index = i + potential_token.__len__()

                        return token

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

    def skip_comments(self):
        tokens = []

        # skip all whitespaces, and comments until the next relevant token is found
        while True:
            lexem = self._next_token()
            if lexem.token != u"/":
                break

            self.push_back()
            comment = self.comment.comment(self)
            if comment is None:
                break

            # take the comment element and add it to the queue of tokens
            tokens.append(comment)

        return tokens
