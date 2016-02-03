class SwiftLexem:
    IDENTIFIER = 1
    IMPLICIT_PARAMETER = 1 << 1
    LITERAL_STRING = 1 << 2
    LITERAL_INTEGER = 1 << 3
    LITERAL_DECIMAL = 1 << 4
    LITERAL_BOOLEAN = 1 << 5
    KEYWORD_DECLARATION = 1 << 6
    KEYWORD_STATEMENT = 1 << 7
    KEYWORD_EXPRESSION_TYPES = 1 << 8
    KEYWORD_PATTERNS = 1 << 9
    KEYWORD_RESERVED = 1 << 10
    PUNCTUATION = 1 << 11

    def __init__(self, cleaned_data, start_position, end_position, type=0):
        self.token = cleaned_data
        self.start_position = start_position
        self.end_position = end_position
        self.type = type
        self.prefix_comments = []

    @classmethod
    def Create(self, lexems, type=0):
        token = u""
        start_position = lexems[0].start_position
        end_position = lexems[0].end_position
        for lexem in lexems:
            if lexem is None:
                continue

            token += lexem.token
            end_position = max(end_position, lexem.end_position)

        return SwiftLexem(token, start_position, end_position, type)

    def __str__(self):
        return "([{0} -> {1}] = {2})".format(self.start_position, self.end_position, self.token)

    def __repr__(self):
        return self.token

    def __eq__(self, other):
        return self.token == other.token and \
               self.start_position == other.start_position and \
               self.end_position == other.end_position
