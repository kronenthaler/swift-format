# TODO: remove all code, rewrite the rules using the parser combinators

from CommentScanner import *
from IdentifierScanner import *


class SwiftScanner:
    EOF = -1000

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
        self.skip()
        id = self.identifier.identifier(self)
        if id is not None:
            id.prefix_comments = prefix_comments

        return id

    def skip(self, charset=string.whitespace):
        for i in range(self.index, len(self.input)):
            if self.input[i] not in charset:
                self.index = i
                break

    def peak_next(self):
        return u"{0}".format(self.input[self.index])

    def next_character(self):
        if self.index >= len(self.input):
            return None

        token = SwiftLexem(u"{0}".format(self.input[self.index]), self.index, self.index)
        self.on_going.insert(0, token)
        self.index += 1
        return token

    def next_chunk(self, skip=string.whitespace, delimiters=string.whitespace + "!\"#$%&'()*+,-./:;<=>?@[\]^`{|}~",
                   allowed_chars=None, allowEOF=False):
        token_payload = u""
        skipping = True
        i = self.index
        for i in range(self.index, len(self.input)):
            if skipping:
                if self.input[i] not in skip:
                    skipping = False
                    token_payload += self.input[i]
                    if (delimiters is not None and self.input[i] in delimiters) or (
                            allowed_chars is not None and self.input[i] not in allowed_chars):
                        return self.insert_token(token_payload, self.index, i, 1)
            else:
                if (delimiters is not None and self.input[i] in delimiters) or (
                        allowed_chars is not None and self.input[i] not in allowed_chars):
                    return self.insert_token(token_payload, self.index, i)

                token_payload += self.input[i]

        if allowEOF:
            return self.insert_token(token_payload, self.index, i)

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

            tok = self.next_chunk(delimiters="{0}".format(target_token[i]), skip=skip)

            tokens_retrieved += 1
            if tok is None or tok.token != u"{0}".format(target_token[i]):
                found = False
                break

            payload += tok.token

        if found:
            token = SwiftLexem(payload, start_position, self.index)
            return self.replace_tokens(token, tokens_retrieved)

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
                        token = self.insert_token(payload, start_position, i, -i)
                        self.insert_token(potential_token, i, i + potential_token.__len__())
                        return token

            payload += self.input[i]

        return None

    def insert_token(self, token_payload, start, end, move_forward=0):
        token = SwiftLexem(token_payload, start, end)
        self.on_going.insert(0, token)
        self.index = end + move_forward
        return token

    def replace_tokens(self, new_token, last_tokens=1):
        self.discard_tokens(last_tokens)
        self.on_going.insert(0, new_token)
        return new_token

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
            lexeme = self.next_chunk()
            if lexeme is None or lexeme.token != u"/":
                break

            self.push_back()
            comment = self.comment.comment(self)
            if comment is None:
                break

            # take the comment element and add it to the queue of tokens
            tokens.append(comment)

        return tokens
